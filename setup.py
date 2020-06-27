"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools.command.install import install
from setuptools import setup, find_packages
from codecs import open
import os
import json
import shutil

from dotenv import load_dotenv
load_dotenv()

curr = os.path.abspath(os.path.dirname(__file__))
home = os.path.expanduser("~")

with open(os.path.join(curr, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='twweet_cli',
    version='2.1.0',
    description='Tweet right from your cli without even opening your browser.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/CruiseDevice/twweet-cli/',
    author='Akash Chavan',
    author_email='achavan1211@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',
    keywords='twitter tweet cli',
    packages=find_packages(),
    install_requires=[
        'tweepy',
        'pyyaml',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'twweet-cli = twweet_cli.main:cli',
        ],
    },
)
