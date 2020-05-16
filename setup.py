from setuptools import setup, find_packages

from pyunormalize import __version__, UNICODE_VERSION

URL = "https://github.com/mlodewijck/pyunormalize"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyunormalize",
    version=__version__,
#    description="Normalization of Unicode text: Pure Python ...",
#    description="Convert Unicode strings to one of the Unicode Normalization Forms.",
#    description="Efficient pure Python Unicode normalization.",
#    description="Unicode normalization forms.",
    description=(
#        "Unicode Normalization Forms. Unicode {} support."
        "A Python implementation of the Unicode Normalization Algorithm "
        "independent from the Python core Unicode database. Unicode {} "
        "support."
        .format(UNICODE_VERSION[:-2])
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    author="Marc Lodewijck",
    author_email="mlodewijck@gmail.com",
    maintainer="Marc Lodewijck",
    maintainer_email="mlodewijck@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=[
        "Unicode",
        "Unicode normalization",
        "normalization",
        "normalization quick check",
        "NFC",
        "NFD",
        "NFKC",
        "NFKD",
        "Unicode Normalization Forms",
        "Unicode Normalization Algorithm",
        "Canonical Ordering Algorithm",
        "Canonical Composition Algorithm",
        "Hangul Syllable Composition Algorithm",
        "Hangul Syllable Decomposition Algorithm",
        "canonical ordering",
        "canonical composition",
        "Hangul syllables",
        "Hangul jamo characters",
    ],
    python_requires=">=3.5",
    packages=find_packages(exclude=["tests", "tools"]),
    include_package_data=True,  # checks MANIFEST.in for explicit rules
    zip_safe=False,
    project_urls={
        "Bug Reports": "{}/issues".format(URL),
        "Source": "{}/".format(URL),
    },
)
