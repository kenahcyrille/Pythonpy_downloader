import subprocess
import os
import shutil
import tempfile
import argparse

def download_package(package_name, version=None, target_dir=None):
    """
    Downloads a specific package and version from PyPI without installing it.

    Args:
        package_name (str): The name of the package to download.
        version (str): The version of the package to download. If None, the latest version will be downloaded.
        target_dir (str): The directory to save the downloaded package. If None, a temporary directory will be used.

    Returns:
        str: The path to the downloaded package.
    """
    if target_dir is None:
        target_dir = tempfile.mkdtemp()

    # Use pip to download the package
    download_command = ['pip', 'download', '--disable-pip-version-check', '-d', target_dir, package_name]
    if version:
        download_command.extend(['==', version])

    try:
        subprocess.check_call(download_command)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to download package {package_name}{' version ' + version if version else ''}.")
        return None

    # Find the downloaded package file
    package_files = [f for f in os.listdir(target_dir) if f.startswith(package_name)]
    if not package_files:
        print(f"Error: No package file found for {package_name}{' version ' + version if version else ''}.")
        return None

    # If multiple package files found, choose the latest one
    package_file = max(package_files)
    package_path = os.path.join(target_dir, package_file)

    return package_path

def download_packages_from_list(file_path, download_dir=None):
    """
    Downloads packages specified in a text file.

    Args:
        file_path (str): The path to the text file containing package names and versions.
        download_dir (str): The directory to save the downloaded packages. If None, a temporary directory will be used.

    Returns:
        list: List of paths to the downloaded package files.
    """
    packages = []
    with open(file_path, 'r') as file:
        for line in file:
            package_info = line.strip().split(',')
            if len(package_info) >= 1:
                package_name = package_info[0]
                version = package_info[1] if len(package_info) >= 2 else None
                package_path = download_package(package_name, version, download_dir)
                if package_path:
                    packages.append(package_path)
    return packages

def main():
    parser = argparse.ArgumentParser(description="Download packages specified in a text file.")
    parser.add_argument("file_path", help="Path to the text file containing package names and versions.")
    parser.add_argument("download_dir", help="Directory to save the downloaded packages.")
    args = parser.parse_args()

    file_path = args.file_path
    download_dir = args.download_dir

    if not os.path.isfile(file_path):
        print("Error: The specified file does not exist.")
        parser.print_usage()
        return

    if not os.path.isdir(download_dir):
        print("Error: The specified download directory does not exist.")
        parser.print_usage()
        return

    downloaded_packages = download_packages_from_list(file_path, download_dir)
    if downloaded_packages:
        print("Packages downloaded successfully:")
        for package_path in downloaded_packages:
            print(package_path)
    else:
        print("No packages were downloaded.")

if __name__ == "__main__":
    main()
