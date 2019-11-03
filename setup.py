"""
github_log_dump - a command line tool for pulling logs from github repositories

See attached README.md file for usage
Copyright: Syncroness, INC - 2019
"""
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='git_log_dump',
    version='0.0.1',
    description='A command line tool for pulling logs from GitHub repositories',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Syncroness-Inc/github_log_dump',
    author='Syncroness, INC',
    author_email='aschafer@syncroness.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['tests']),  # Required
    python_requires='>=3.7, <4',
    install_requires=['github', 'yaml', 'progressbar'],  # Optional
    entry_points={  # Optional
        'console_scripts': [
            'github_log_dump=github_log_dump:cmdline',
        ],
    },
)
