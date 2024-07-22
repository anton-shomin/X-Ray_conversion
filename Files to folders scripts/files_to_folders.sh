#!/bin/bash

# get directory where the script is located
dir_path="$PWD"

# change directory to dir_path
cd "$dir_path"

# loop through all files in the directory
for file in *; do
    # skip directories and "files_to_folder" file
    if [[ -d $file ]] || [[ $file == "files_to_folder" ]]; then continue; fi

    # get file name without extension
    filename="${file%.*}"

    # create new directory with filename, -p flag is used to avoid error if directory already exists
    mkdir -p "$filename"

    # move file to the new directory
    mv "$file" "$filename"
done