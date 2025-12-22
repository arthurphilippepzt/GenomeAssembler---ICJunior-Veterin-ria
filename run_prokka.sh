#!/bin/bash

# Default values
organize=false
cpus=8  # default CPU count

usage() {
  echo "Usage: $0 -i <input_dir> -T <threads> [-o] [-h]"
  echo ""
  echo "Options:"
  echo "  -i <input_dir>   Directory containing input files (required)"
  echo "  -T <threads>     Number of CPU threads to use (default = 8)"
  echo "  -o               Organize .faa and .gbk outputs into separate folders"
  echo "  -h               Show this help message and exit"
}

# Parse command-line arguments
while getopts ":i:T:oh" opt; do
  case $opt in
    i) input_dir="$OPTARG" ;;
    T) cpus="$OPTARG" ;;
    o) organize=true ;;  # Optional flag, doesn't take an argument
    h) usage; exit 0 ;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2; exit 1 ;;
  esac
done

# Check prokka instalation
if ! command -v prokka > /dev/null 2>&1; then
    echo "Error: check prokka instalation or environment activation" >&2
    exit 1
fi

# Check required options
if [[ -z "$input_dir" ]]; then
  echo "Error: -i option required." >&2
  usage
  exit 1
fi


#Debug prints (optional)
echo "Input directory: $input_dir"
echo "CPUs: $cpus"
echo "Organize files: $organize"

echo -e "\n###############################"
echo -e "\033[33m\040\040\040Running automated prokka\033[0m"
echo -e "###############################"

# creating directories
results_dir="$input_dir/results/"
mkdir -p "$results_dir"
# Count total number of files to process
total_files=$(find "$input_dir" -maxdepth 1 -type f \
  \( -name "*.fna" -o -name "*.fa" -o -name "*.fasta" \) | wc -l)


current=0

if (( total_files == 0 )); then
    echo "No files found in $input_dir"
    exit 1
fi

# Process files
find "$input_dir" -maxdepth 1 -type f -print0 | while IFS= read -r -d '' assembly_file; do

    ### actual code ###
    filename=$(basename "$assembly_file")
    base_filename="${filename%.*}"  # Remove extension

    echo -e "\nProcessing file $filename"


    if strain_name=$(python3 get_bac_name.py "$assembly_file" 2>/dev/null); then
	echo -e "Running $strain_name"
    else
        strain_name="$base_filename"
        echo -e "Running $strain_name"
    fi

    if prokka --addgenes --outdir "$results_dir/$base_filename" --prefix "$strain_name" --cpus "$cpus" --force --quiet "$assembly_file" > /dev/null 2>&1 ; then
        echo -e "\033[32m✓ Success\033[0m"
    else
        echo -e "\033[31m✗ Failed\033[0m" >&2
    fi

    ((current ++))

    if ((current>0)); then
        ### Progress bar ###
        # Calculate progress
        percent=$((current * 100 / total_files))

        printf "\r[%-50s] %3d%% (%d/%d)" \
            $(printf "#%.0s" $(seq 1 $((percent/2)))) \
            "$percent" "$current" "$total_files"
    fi

    echo -e ""

done
echo -e "\n"

if $organize; then

echo -e "Creating faa and gbk directories"
faa_dir="$results_dir/faa_files"
gbk_dir="$results_dir/gbk_files"

mkdir -p "$faa_dir" "$gbk_dir"

    echo -e "\nRunning file organization...\n"
  
   #Move .faa files
    find "$results_dir" -type f -name "*.faa" -print0 | while IFS= read -r -d '' faa_file; do
        base=$(basename "$faa_file")
        target="$faa_dir/$base"
    
        if [[ -e "$target" ]]; then
            echo -e "\033[31mWarning\033[0m: '$base' already exists in '$faa_dir'. Skipping."
        else
            mv "$faa_file" "$target"
        fi
    done

# Move .gbk files
    find "$results_dir" -type f -name "*.gbk" -print0 | while IFS= read -r -d '' gbk_file; do
        base=$(basename "$gbk_file")
        target="$gbk_dir/$base"
    
        if [[ -e "$target" ]]; then
            echo -e "\033[31mWarning\033[0m: '$base' already exists in '$gbk_dir'. Skipping."
        else
            mv "$gbk_file" "$target"
        fi
    done

echo -e "\nFile organization completed!"
echo -e "\n"
fi

echo -e "#####################################################"
echo -e "\033[33m\040\040\040Script finished running, thank you for using it!\033[0m"
echo -e "#####################################################"
