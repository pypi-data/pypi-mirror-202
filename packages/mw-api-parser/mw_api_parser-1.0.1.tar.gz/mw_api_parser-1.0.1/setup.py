import setuptools
import sys

if sys.version_info < (3, 11):
    raise RuntimeError("This package requires Python 3.11 or later!")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mw_api_parser",
    version="1.0.1",
    author="Jerry White",
    author_email="MidwayVI@surry.net",
    description="Python wrapper to help parse the Merriam-Webster API response",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whitej27030/MW_API_Parser.git",
    packages=setuptools.find_packages(),

    classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
    ],

    install_requires=[
        'python-dotenv>=0.21.0',
],

    python_requires=">=3.11",
)
