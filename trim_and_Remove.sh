#!/bin/bash

# Define the number of threads, input, and output directories
# "./" stands for current directory
trimgalore_threads=10
INPUT_DIR="./"
OUTPUT_DIR="./trimming_output"
SRR_LIST="noresult_fm.txt"
ERROR_LOG="error_log.txt"

# Create input and output directories if they don't exist
mkdir -p "$INPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Create or clear the error log file
> "$ERROR_LOG"

# Loop over each SRR ID, trim the FASTQ files, and delete the originals
while read -r srr_id; do
    echo "Trimming files for $srr_id..."
    
    # Get the downloaded FASTQ files
    for FILE in "$INPUT_DIR/${srr_id}"*.fastq; do
        if [ -f "$FILE" ]; then
            echo "Processing $FILE with Trim Galore..."
            trim_galore --cores "$trimgalore_threads" --output_dir "$OUTPUT_DIR" "$FILE"

            if [ $? -eq 0 ]; then
                # Remove the original FASTQ file
                echo "Removing original FASTQ file $FILE..."
                rm "$FILE"
                if [ $? -ne 0 ]; then
                    echo "Error: failed to remove $FILE." | tee -a "$ERROR_LOG"
                fi
            else
                echo "Error: failed to trim $FILE with Trim Galore." | tee -a "$ERROR_LOG"
            fi
        else
            echo "Warning: No FASTQ files found for $srr_id." | tee -a "$ERROR_LOG"
        fi
    done
done < "$SRR_LIST"

echo "Trimming and removal process completed."
echo "Errors occurred for the following SRR IDs (if any):"
cat "$ERROR_LOG"

