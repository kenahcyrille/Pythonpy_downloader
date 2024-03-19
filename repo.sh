The update_repo.sh script should run download.py with the package list file and output directory provided to download.py (see #5). It should then rerun createrepo in the pypi repo directory to include the new packages.

It will make sense, to have fixed values but overridable values (via environment variables) in update_repo.sh for the package list file and the output directory:

PYPI_PACKAGE_LIST=${PYPI_PACKAGE_LIST:-"package_list.txt"}
PYPI_REPO_DIR=${PYPI_REPO_DIR:-"/path/to/repo/dir"}
update_repo.sh should also loop over each supported python version and run download.py to make sure that any python version specific packages are included in the repo. We'll want to have something like

PYTHON_VERSIONS=( 3.9 3.10 3.11 3.12 )

for version in ${PYTHON_VERSIONS[@]}
do
    ml python/${version}   
    ./download.py <package-list> <repo-dir>
done
Any packages that are not version specific should automatically be skipped by pip if they already exist.
