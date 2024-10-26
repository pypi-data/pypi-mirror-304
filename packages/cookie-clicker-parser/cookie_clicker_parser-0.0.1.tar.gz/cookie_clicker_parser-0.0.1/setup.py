from setuptools import setup, find_packages

VERSION = "0.0.1" 
DESCRIPTION = "My first Python package"
LONG_DESCRIPTION = "My first Python package with a slightly longer description"

setup(
        name="cookkkkkie-clicker-parser", 
        version=VERSION,
        author="ShadowCrafter",
        author_email="lkoe@bluewin.ch",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],

        keywords=["python", "cookie clicker"],
        classifiers= [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independant"
        ]
)
