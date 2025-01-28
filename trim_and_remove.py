import os
import subprocess

# Define the number of threads, input, and output directories
fasterq_threads = 60
trimgalore_threads = 30
INPUT_DIR = "./fastq_files"
OUTPUT_DIR = "./trimming_output"
SRR_LIST = "noresult_fm.txt"
ERROR_LOG = "error_log.txt"

# Create input and output directories if they don't exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Create or clear the error log file
with open(ERROR_LOG, 'w') as error_log:
    error_log.write("")

# Loop over each SRR ID, download the FASTQ files, and trim them
with open(SRR_LIST, 'r') as srr_file:
    for srr_id in srr_file:
        srr_id = srr_id.strip()  # Remove any leading/trailing whitespace
        print(f"Downloading {srr_id}...")
        
        # Download the FASTQ files
        download_command = f"fasterq-dump --progress -e {fasterq_threads} {srr_id} -O {INPUT_DIR}"
        try:
            subprocess.run(download_command, shell=True, check=True)
            print(f"Download complete for {srr_id}. Starting trimming...")
            
            # Get the downloaded FASTQ files
            for file in os.listdir(INPUT_DIR):
                if file.startswith(srr_id) and file.endswith('.fastq'):
                    file_path = os.path.join(INPUT_DIR, file)
                    print(f"Processing {file_path} with Trim Galore...")
                    
                    # Trim the FASTQ files
                    trim_command = f"trim_galore --cores {trimgalore_threads} --output_dir {OUTPUT_DIR} {file_path}"
                    try:
                        subprocess.run(trim_command, shell=True, check=True)
                        
                        # Remove the original FASTQ file
                        print(f"Removing original FASTQ file {file_path}...")
                        os.remove(file_path)
                    except subprocess.CalledProcessError:
                        with open(ERROR_LOG, 'a') as error_log:
                            error_log.write(f"Error: failed to trim {file_path} with Trim Galore.\n")
                        print(f"Error: failed to trim {file_path} with Trim Galore.")
                    except OSError:
                        with open(ERROR_LOG, 'a') as error_log:
                            error_log.write(f"Error: failed to remove {file_path}.\n")
                        print(f"Error: failed to remove {file_path}.")
        except subprocess.CalledProcessError:
            with open(ERROR_LOG, 'a') as error_log:
                error_log.write(f"Error: failed to download {srr_id}.\n")
            print(f"Error: failed to download {srr_id}.")

print("Download, trimming, and removal process completed.")
print("Errors occurred for the following SRR IDs (if any):")
with open(ERROR_LOG, 'r') as error_log:
    print(error_log.read())
