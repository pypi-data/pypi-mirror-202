import argparse
import os
import sys
import tempfile
import zipfile
import tarfile
import requests
from pathlib import Path
from typing import List
import subprocess

def extract_requirements(package_path: str) -> List[str]:
    requirements = []

    if package_path.endswith(".whl"):
        with zipfile.ZipFile(package_path) as zfile:
            for name in zfile.namelist():
                if name.endswith("requirements.txt"):
                    with zfile.open(name) as req_file:
                        requirements.extend(
                            req.strip().decode() for req in req_file.readlines()
                        )
    elif package_path.endswith(".tar.gz"):
        with tarfile.open(package_path) as tfile:
            for member in tfile.getmembers():
                if member.name.endswith("requirements.txt"):
                    req_file = tfile.extractfile(member)
                    if req_file:
                        requirements.extend(
                            req.strip().decode() for req in req_file.readlines()
                        )

    return requirements

def is_package_installed(package_name: str) -> bool:
    try:
        subprocess.run(["pip", "show", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_dependencies(dependencies: List[str]):
    for dependency in dependencies:
        if not is_package_installed(dependency):
            subprocess.run(["pip", "install", dependency], check=True)

def install_package_from_path(package_path: str):
    requirements = extract_requirements(package_path)
    install_dependencies(requirements)
    subprocess.run(["pip", "install", package_path], check=True)

def install_package_from_pypi(package_name: str):
    with tempfile.TemporaryDirectory() as tempdir:
        subprocess.run(["pip", "download", "--no-deps", "--no-binary", ":all:", "-d", tempdir, package_name], check=True)

        package_files = [f for f in Path(tempdir).iterdir() if f.is_file()]

        if not package_files:
            print(f"Error: Package {package_name} not found.")
            sys.exit(1)

        for package_file in package_files:
            install_package_from_path(str(package_file))

def main():
    parser = argparse.ArgumentParser(description="instareq: A Python package installer with dependency resolution.")
    parser.add_argument("package", nargs="?", help="Path to the package file or package name.")
    
    args = parser.parse_args()

    if not args.package:
        parser.print_help()
        sys.exit(1)

    package = args.package.strip()

    if os.path.isfile(package):
        install_package_from_path(package)
    else:
        install_package_from_pypi(package)


if __name__ == "__main__":
    main()
