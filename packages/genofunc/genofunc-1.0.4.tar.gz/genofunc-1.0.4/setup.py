from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory/"README.md").read_text()

setup(
    name="genofunc",
    version="1.0.4",
    packages=find_packages(),
    url="https://github.com/xiaoyu518/genofunc",
    license="MIT",
    entry_points={"console_scripts": ["genofunc = genofunc.__main__:main"]},
    test_suite="nose.collector",
    tests_require=["nose >= 1.3"],
    install_requires=[
        "biopython>=1.70",
        "numpy>=1.18",
        "pandas>=0.24.2",
        "nextstrain-augur>=13.1.2",
        "mappy>=2.24",
        "parasail>=1.2.4"
    ],
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
    ],
)
