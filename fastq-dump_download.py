import os
import subprocess

# Define the input file containing SRR IDs
SRR_LIST = "srr_id.txt"
OUTPUT_DIR = "downloaded_fastq_files"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Loop over each SRR ID, download the FASTQ files
with open(SRR_LIST, 'r') as srr_file:
    for srr_id in srr_file:
        srr_id = srr_id.strip()  # Remove any leading/trailing whitespace
        print(f"Downloading {srr_id}...")

        # Download the FASTQ files using fastq-dump
        download_command = f"fastq-dump --outdir {OUTPUT_DIR} --split-files --origfmt {srr_id}"
        
        try:
            subprocess.run(download_command, shell=True, check=True)
            print(f"Download complete for {srr_id}.")
        except subprocess.CalledProcessError as e:
            print(f"Error: failed to download {srr_id}. Error: {e}")

print("All downloads attempted.")

