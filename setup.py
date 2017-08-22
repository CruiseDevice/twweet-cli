"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='twweet_cli',
    version='1.0.0',

    description='Tweet right from your cli without even opening your browser.',
    long_description=long_description,
    
    url='https://github.com/CruiseDevice/twweet-cli/',

    author='Akash Chavan',
    author_email='achavan1211@gmail.com',

    license='MIT',
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
    ],

    keywords='twitter tweet cli',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
         'tweepy',
     ],
    
     py_modules=["twweet_cli"],
     entry_points={
        'console_scripts': [
            'twweet-cli = twweet_cli:main',
        ],
     }
)
