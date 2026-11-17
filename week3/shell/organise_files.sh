#!/usr/bin/env bash

if [ $# -ne 1 ] || [ ! -d "$1" ]; then
    echo "Usage: $0 <folder>"
    exit 1
fi

folder="${1%/}"        # also tolerates a trailing slash
today=$(date +%F)
count=0

for f in "$folder"/*; do
    if [ -f "$f" ]; then
        base=$(basename "$f")
        case "$base" in
            "${today}_"*) continue ;;     # already renamed today, skip
        esac
        newname=$(echo "$base" | tr -s ' ' | tr 'A-Z ' 'a-z_')
        mv -n "$f" "$folder/${today}_${newname}"   # -n never overwrites an existing file
        count=$((count + 1))
    fi
done

archive="$(dirname "$folder")/$(basename "$folder")_${today}.tar.gz"
tar czf "$archive" -C "$(dirname "$folder")" "$(basename "$folder")" || exit 1

echo "Renamed $count files"
echo "Created archive: $archive"