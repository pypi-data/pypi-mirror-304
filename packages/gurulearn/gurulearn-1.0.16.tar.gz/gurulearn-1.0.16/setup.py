from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='gurulearn',
    version='1.0.16',
    description='library for linear_regression and multi image model',
    author='Guru Dharsan T',
    author_email='gurudharsan123@gmail.com',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
    'opencv-python',
    'scipy',
    'matplotlib',
    'tensorflow==2.16.1',
    'keras',
    'pandas',
    'numpy',
    'plotly',
    'scikit-learn',
    'librosa',
    'tqdm',
    'resampy',
    'pillow',
    'xgboost'
    ],
)
