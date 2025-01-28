#!/bin/bash

# Define the number of threads, input, and output directories

fasterq_threads=60
trimgalore_threads=30
INPUT_DIR="./fastq_files"
OUTPUT_DIR="./trimming_output"
SRR_LIST="noresult_fm.txt"
ERROR_LOG="error_log.txt"

# Create input and output directories if they don't exist
mkdir -p $INPUT_DIR
mkdir -p $OUTPUT_DIR

# Create or clear the error log file
> $ERROR_LOG

# Loop over each SRR ID, download the FASTQ files, and trim them
while read -r srr_id; do
    echo "Downloading $srr_id..."
    fasterq-dump --progress -e $fasterq_threads $srr_id -O $INPUT_DIR

    if [ $? -eq 0 ]; then
        echo "Download complete for $srr_id. Starting trimming..."
        # Get the downloaded FASTQ files
        for FILE in $INPUT_DIR/${srr_id}*.fastq; do
            echo "Processing $FILE with Trim Galore..."
            trim_galore  --cores $trimgalore_threads --output_dir $OUTPUT_DIR $FILE

            if [ $? -eq 0 ]; then
                # Remove the original FASTQ file
                echo "Removing original FASTQ file $FILE..."
                rm $FILE
                if [ $? -ne 0 ]; then
                    echo "Error: failed to remove $FILE." | tee -a $ERROR_LOG
                fi
            else
                echo "Error: failed to trim $FILE with Trim Galore." | tee -a $ERROR_LOG
            fi
        done
    else
        echo "Error: failed to download $srr_id." | tee -a $ERROR_LOG
    fi
done < $SRR_LIST

echo "Download, trimming, and removal process completed."
echo "Errors occurred for the following SRR IDs (if any):"
cat $ERROR_LOG

