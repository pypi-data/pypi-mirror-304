"""
Setup script for Polaris.

A Unified Axial-aware Framework for Chromatin Loop Annotation in Bulk and Single-cell Hi-C Data
"""

from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_des = readme.read()

setup(
    name='polaris-loop',
    version='0.1.0',
    author="Yusen HOU, Yanlin Zhang",
    author_email="yhou925@connect.hkust-gz.edu.cn",
    description="A Unified Axial-aware Framework for Chromatin Loop Annotation in Bulk and Single-cell Hi-C Data",
    long_description=long_des,
    long_description_content_type="text/markdown",
    url="https://github.com/compbiodsa/Polaris",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pip==24.0',
        'setuptools==75.1.0',
        'accelerate==0.34.2',
        'deepspeed==0.15.1',
        'tensorboard==2.17.1',
        'appdirs==1.4.4',
        'click==8.0.1',
        'cooler==0.8.11',
        'matplotlib==3.8.0',
        'numpy==1.22.4',
        'pandas==1.3.0',
        'scikit-learn==1.4.2',
        'scipy==1.7.3',
        'timm==0.6.12',
        'torch==2.2.2',
        'torch-ema==0.3',
        'tqdm==4.65.0',
    ],
    entry_points={
        'console_scripts': [
            'polaris = polaris.polaris:cli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
