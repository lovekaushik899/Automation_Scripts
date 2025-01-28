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
