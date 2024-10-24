__author__ = 'Sujit Mandal'
#Date :24-10-2024
from setuptools import setup 

def readme():
    with open('README.md') as files:
        README = files.read()

    return(README)

setup(
    name = 'check-internet-speed',
    version = '0.0.2',
    description = "checking internet upload and download speed.",
    long_description = readme(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/sujitmandal/check-internet-speed',
    author = 'Sujit Mandal',
    author_email = 'mandals974@gmail.com',
    license = 'MIT',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],


    packages = ['check_internet_speed'],
    include_package_data = True,
)
