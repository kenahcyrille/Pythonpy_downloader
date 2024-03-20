#!/bin/bash

# Default values for package list file and output directory
PYPI_PACKAGE_LIST=${PYPI_PACKAGE_LIST:-"package_list.txt"}
PYPI_REPO_DIR=${PYPI_REPO_DIR:-"/path/to/repo/dir"}

# Supported Python versions
PYTHON_VERSIONS=(3.9 3.10 3.11 3.12)

# Loop over each supported python version and run download.py
for version in "${PYTHON_VERSIONS[@]}"
do
    # Activate the Python version
    ml python/${version}

    # Run download.py with package list and repo directory
    python_script="download_packages.py"

    while getopts ":f:d:" opt; do
        case $opt in
            f)  # Specify the package list file
                package_list_file="$OPTARG"
                ;;
            d)  # Specify the download directory
                download_dir="$OPTARG"
                ;;
            \?) # Invalid option
                echo "Invalid option: -$OPTARG" >&2
                ;;
        esac
    done

    shift $((OPTIND -1))

    python3 "$python_script" -f "$package_list_file" -d "$download_dir"
done
