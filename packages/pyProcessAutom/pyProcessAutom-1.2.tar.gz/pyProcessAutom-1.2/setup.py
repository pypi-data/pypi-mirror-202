from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyProcessAutom',
    version='1.2',
    description='A data preprocessing library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Aryan Sakhala',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn'
    ],
)
