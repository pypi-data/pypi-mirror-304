from setuptools import setup, find_packages

setup(
    name='fastmodels-kit',
    version='0.1.0',
    description='A command-line interface for interacting with FastModel product and services.',
    packages=find_packages(),
    install_requires=[
        'jsonschema', 'requests'
    ],
    entry_points={
        'console_scripts': [
            'fastmodels=fastmodels.cli:main',
            'fastmodels-open=fastmodels.cli:main',
        ],
    },
)
