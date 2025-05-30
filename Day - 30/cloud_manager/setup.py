# setup.py
from setuptools import setup, find_packages

setup(
    name="cloud_manager",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'boto3',
        'click',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'cloud-manager=cloud_manager.cli:cli',
        ],
    },
)
