while read -r srr_id; do
	echo "Downloading $srr_id.."
	fasterq-dump $srr_id --progress --split-files -e 30
    
done < srr_id.txt
