from setuptools import setup, find_packages

setup(
    # Application name:
    name="cognitiveatlas",

    # Version number (initial):
    version="0.1.3",

    # Application author details:
    author="Poldracklab",
    author_email="vsochat@stanford.edu",

    # Packages
    packages=["cognitiveatlas"],

    # Data
    package_data = {'cognitiveatlas':['html/*.html','data/*.csv']},

    # Details
    url="https://github.com/CognitiveAtlas/cogat-python",

    license="MIT",
    description="python wrapper for the cognitive atlas (cognitiveatlas.org) RESTful API",

    keywords='cogniive atlas cognition behavioral paradigm ontology',

    install_requires = ["numpy","pandas","future"]

)
