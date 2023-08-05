from setuptools import setup

VERSION = "0.0.2"

with open("README.md", "r") as fp:
    README = fp.read()

setup(
    name="unhandled_exception_logger",
    version=VERSION,
    description="Log unhandled exceptions as critical",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Chris Simpson",
    author_email="oss@karmacomputing.co.uk",
    url="https://github.com/karmacomputing/unhandled_exception",
    py_modules=["unhandled_exception_logger"],
    classifiers=["License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
)
