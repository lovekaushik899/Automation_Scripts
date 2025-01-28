import os
import subprocess

# Define the input file containing SRR IDs
SRR_LIST = "srr_id.txt"

# Loop over each SRR ID, download the FASTQ files
with open(SRR_LIST, 'r') as srr_file:
    for srr_id in srr_file:
        srr_id = srr_id.strip()  # Remove any leading/trailing whitespace
        print(f"Downloading {srr_id}...")
        
        # Download the FASTQ files
        download_command = f"fasterq-dump {srr_id} --progress --split-files -e 30"
        try:
            subprocess.run(download_command, shell=True, check=True)
            print(f"Download complete for {srr_id}.")
        except subprocess.CalledProcessError as e:
            print(f"Error: failed to download {srr_id}. Error: {e}")

print("All downloads attempted.")
