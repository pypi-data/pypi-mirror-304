from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='test-calc-pkg-mic', # name of the package that will be on the repository -> has to be unique in the repository.
    version='0.0.2',
    # url,
    author='Michael Vella',
    # author_email,
    description='Simple test package creation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[]
)