from setuptools import setup, find_packages

setup(
    name='fastmodels-kit',
    version='0.1.1',
    description='A command-line interface for interacting with FastModel product and services.',
    packages=find_packages(),
    install_requires=[
        'jsonschema', 'requests'
    ]
)
