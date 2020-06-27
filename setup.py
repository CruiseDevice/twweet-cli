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

here = os.path.abspath(os.path.dirname(__file__))
home = os.path.expanduser("~")

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class TwtApiDetails(install):
    def run(self):
        print("Creating Data Directories...")
        check_data_dir_exists()
        create_creds()
        print("""Creating default config files.
              Please note that this overwrites the files if exist....""")
        with open(home + '/.twweet-cli/data/config.yml', 'w') as ymlfile:
            ymlLine1 = "#Depending on the system(Windows or Linux) change the\
                             backward or forward slash appropriately."
            ymlLine2 = "Tweets: /TweetsStore/"
            ymlLine3 = "HashTag: /HashTagStore/"
            ymlfile.write("%s\n%s\n%s\n" % (ymlLine1, ymlLine2, ymlLine3))
            install.run(self)


def check_data_dir_exists():
    try:
        original_umask = os.umask(0)
        if os.path.exists(home + '/.twweet-cli/data'):
            response = input("""The data directory already exists.
                             Would you like to overwrite? [yes/no] : """)
            if response.lower() == 'yes':
                shutil.rmtree(home + '/.twweet-cli/data')
                os.makedirs(home + '/.twweet-cli/data')
            elif response.lower() == 'no':
                print("Not overwriting...")
    except OSError:
        print("Cannot create data dir the installation cannot continue..")
        exit()
    finally:
        os.umask(original_umask)


def create_creds():
    try:
        jsondata = {
            "consumer_key": os.environ["CONSUMER_KEY"].strip(),
            "consumer_secret": os.environ["CONSUMER_SECRET"].strip(),
            "access_token": os.environ["ACCESS_TOKEN"].strip(),
            "access_token_secret": os.environ["ACCESS_TOKEN_SECRET"].strip()
        }
    except Exception as e:
        print("Make sure to set your Twitter OAuth credentials in your .env\
                 file. Refer to Readme for project setup.")
        raise e
    with open(home + "/.twweet-cli/data/creds.json", "w") as outfile:
        json.dump(jsondata, outfile)
    os.chmod(home + '/.twweet-cli/data/creds.json', 0o777)


setup(
    name='twweet_cli',
    version='2.0.6',
    description='Tweet right from your cli without even opening your browser.',
    long_description=long_description,
    url='https://github.com/CruiseDevice/twweet-cli/',
    author='Akash Chavan',
    author_email='achavan1211@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={
        'install': TwtApiDetails,
    },
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
