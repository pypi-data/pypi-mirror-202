import pathlib
from setuptools import setup, find_packages

# Read the contents of the README.md file
here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text()

setup(
    name="InstaReq",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "instareq = instareq:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mubarak Alketbi",
    author_email="mubarak.harran@gmail.com",
    url="https://github.com/MHketbi/InstaReq",
    license="GPLv3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
