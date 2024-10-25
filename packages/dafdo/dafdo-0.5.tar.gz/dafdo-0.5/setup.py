# setup.py

from setuptools import setup, find_packages

setup(
    name='dafdo',
    version='0.5',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dafdo=dafdo.__init__:main',
        ],
    },
    install_requires=[],
)
