# setup.py

from setuptools import setup, find_packages

setup(
    name='interfusion_encoder',
    version='0.1.0',
    description='A package for training and inference of the InterFusion Encoder model',
    author='Edward Liu',
    author_email='edwardliu01@gmail.com',
    packages=find_packages(),
    install_requires=[
        'torch>=1.7.0',
        'transformers>=4.0.0',
        'numpy',
        'pandas',
        'tqdm',
        'wandb',
    ],
    python_requires='>=3.6',
)

