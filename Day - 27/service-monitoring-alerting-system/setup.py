from setuptools import setup, find_packages

setup(
    name="service-monitor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'retry>=0.9.2',
        'PyYAML>=5.4.1'
    ],
    entry_points={
        'console_scripts': [
            'service-monitor=src.monitor:main',
        ],
    },
)
