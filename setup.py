from setuptools import setup, find_packages

setup(
    # Application name:
    name="cognitiveatlas",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Poldracklab",
    author_email="vsochat@stanford.edu",

    # Packages
    packages=["cognitiveatlas"],

    # Data
    package_data = {'cognitiveatlas':['html/*.html','data/*.csv']},

    # Details
    url="http://www.cognitiveatlas.org",

    license="LICENSE.txt",
    description="python functions to use cognitive atlas",

    install_requires = ["pandas","rdflib"]

)
