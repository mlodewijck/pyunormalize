"""Setup script for pyunormalize."""

import os
from setuptools import setup, find_packages

URL = "https://github.com/mlodewijck/pyunormalize"


def get_version():
    version_file = os.path.join("pyunormalize", "_version.py")
    namespace = {}
    with open(version_file, encoding="utf-8") as f:
        exec(compile(f.read(), version_file, "exec"), namespace)
    return namespace["__version__"]


with open("README.md", encoding="utf-8") as f:
    README = f.read()


setup(
    name="pyunormalize",
    version=get_version(),
    description=(
        "A library for Unicode normalization (NFC, NFD, NFKC, NFKD) "
        "independent of Python's core Unicode database."
    ),
    long_description=README,
    long_description_content_type="text/markdown",
    author="Marc Lodewijck",
    author_email="mlodewijck@gmail.com",
    license="MIT",  # SPDX expression
    url=URL,
    project_urls={
        "Bug Reports": f"{URL}/issues",
        "Source": f"{URL}/",
    },
    keywords=[
        "nfc",
        "nfd",
        "nfkc",
        "nfkd",
        "normalization forms",
        "normalize",
        "hangul",
        "text",
        "text processing",
        "unicode",
        "unicode normalization",
        "i18n",
        "python",
        "pure-python",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    packages=find_packages(exclude=["tests", "*.tests"]),
    include_package_data=True,
    zip_safe=False,
)
