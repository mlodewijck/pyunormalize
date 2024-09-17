"""Setup script for pyunormalize."""

import os
from setuptools import setup, find_packages

URL = "https://github.com/mlodewijck/pyunormalize"


def get_version():
    version_file = os.path.join("pyunormalize", "_version.py")
    namespace = {}
    with open(version_file) as f:
        exec(compile(f.read(), version_file, "exec"), namespace)
    return namespace["__version__"]

with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="pyunormalize",
    version=get_version(),
    description=(
        "Unicode normalization forms (NFC, NFKC, NFD, NFKD). A library "
        "independent of the Python core Unicode database."
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    author="Marc Lodewijck",
    author_email="mlodewijck@gmail.com",
    license="MIT",
    url=URL,
    project_urls={
        "Bug Reports": "{}/issues".format(URL),
        "Source": "{}/".format(URL),
    },
    keywords=[
        "Unicode",
        "Unicode data",
        "Unicode normalization",
        "normalization",
        "NFC",
        "NFD",
        "NFKC",
        "NFKD",
        "Unicode Normalization Forms",
        "Canonical Ordering Algorithm",
        "Canonical Composition Algorithm",
        "canonical ordering",
        "canonical composition",
        "Hangul Syllable Composition Algorithm",
        "Hangul Syllable Decomposition Algorithm",
        "Hangul syllables",
        "Hangul jamo characters",
    ],
    # Trove classifiers
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    # All data files matched by MANIFEST.in will get included
    # if they are inside a package directory.
    zip_safe=False,
)
