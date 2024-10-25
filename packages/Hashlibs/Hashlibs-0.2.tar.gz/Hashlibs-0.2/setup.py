# setup.py

from setuptools import setup, find_packages

setup(
    name='Hashlibs',
    version='0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'my_experiments = main:main',
        ],
    },
)
