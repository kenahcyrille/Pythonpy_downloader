import subprocess
import os
import shutil
import tempfile

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

# Example usage
package_name = 'requests'
version = '2.25.1'
download_dir = '/path/to/save/packages'

package_path = download_package(package_name, version, download_dir)
if package_path:
    print(f"Package downloaded successfully: {package_path}")
else:
    print("Failed to download package.")
