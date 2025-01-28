while read -r srr_id; do
    fastq-dump --outdir downloaded_fastq_files --split-files --origfmt $srr_id
done < srr_id.txt
