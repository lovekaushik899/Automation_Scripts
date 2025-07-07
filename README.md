# 🔧 Automation Scripts for NGS Data Processing

This repository contains a collection of bash scripts for automating common NGS data processing tasks, including data download from NCBI, trimming, alignment, and post-processing. Each task is available in both sequential and parallel versions, with detailed logging enabled.

---

## 📦 Dependencies

Ensure the following tools are installed and accessible in your environment:

- **sratoolkit** (for `prefetch`, `fasterq-dump`)
- **Trim Galore**
- **GNU Parallel**
- **BWA**
- **SAMtools**
- **Coreutils** (for utilities like `date`, `mkdir`, etc.)

Install via conda or package manager:
```bash
conda install -c bioconda sra-tools trim-galore parallel bwa samtools


| Tool           | Purpose                                                 |
| -------------- | ------------------------------------------------------- |
| `prefetch`     | Downloads `.sra` files from NCBI SRA                    |
| `fasterq-dump` | Converts `.sra` files to `.fastq` format                |
| `Trim Galore`  | Performs adapter and quality trimming on `.fastq` files |
| `BWA mem`      | Aligns `.fastq` reads to a reference genome             |
| `SAMtools`     | Converts SAM to BAM, sorts, and indexes BAM files       |
| `GNU Parallel` | Enables parallel execution of batch processing commands |
```bash


**1_sequential_download_convert.sh:**
Sequentially downloads SRA files and converts them to FASTQ using `fasterq-dump`.            
**2_parallel_download_convert.sh:**
Downloads SRA files and converts to FASTQ in parallel using `GNU Parallel`.                  
**3_parallel_trim_galore.sh:**
Trims FASTQ files in parallel using `Trim Galore`.                                           
**4_sequential_trim_galore.sh:**
Trims FASTQ files sequentially using `Trim Galore`.                                          
**5_sequential_bwa_alignment.sh:**
Aligns trimmed reads to the reference genome sequentially using `BWA mem`.                  
**6_parallel_bwa_alignment.sh:**
Aligns trimmed reads to the reference genome in parallel using `BWA mem` and `GNU Parallel`. 
**7_sequential_bam_processing.sh:**
Converts SAM to BAM, sorts and indexes BAM files sequentially using `SAMtools`.              
**8_parallel_bam_processing.sh:**
Performs SAM to BAM conversion, sorting and indexing in parallel using `GNU Parallel`.       
