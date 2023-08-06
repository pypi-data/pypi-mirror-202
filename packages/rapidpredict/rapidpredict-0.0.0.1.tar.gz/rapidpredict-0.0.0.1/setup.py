from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.0.1'
DESCRIPTION = 'rapid predict is a python package to simplifies the process of fitting and evaluating multiple machine learning models on a dataset.'
LONG_DESCRIPTION = 'This repository contains a Python-based framework for rapid prediction of machine learning models\
      that simplifies the process of fitting and evaluating multiple machine learning models from scikit-learn.\
          It''s designed to provide a quick way to test various algorithms on a given dataset and compare their performance.'

# Setting up
setup(
    name="rapidpredict",
    version=VERSION,
    author="Synthetic Dataset AI Team",
    author_email="<admin@syntheticdataset.ai>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['python', 'pandas', 'numpy', 'scikit-learn', 'scipy', 'matplotlib', 'seaborn', 'tqdm'],
    keywords=['python', 'pandas', 'numpy', 'scikit-learn', 'scipy', 'matplotlib', 'seaborn'],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: Free To Use But Restricted",

    ] ,
)
