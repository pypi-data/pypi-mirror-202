from setuptools import setup, find_packages
import os

__version__ = "Undefined"
for line in open(os.path.join("puploader", "__init__.py")):
    if line.startswith("__version__"):
        exec(line.strip())


setup(
    name='puploader',
    version=__version__,
    description="A command line tool to push data to "
                "the Polarplot dedicated AWS S3 bucket for D-ICE Engineering needs.",

    author="Omar El Bakouchi",
    author_email="omar.elbakouchi@dice-engineering.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
    ],
    packages=find_packages(),
    install_requires=[
        'boto3',
    ],
    entry_points={
        'console_scripts': [
            'puploader=puploader.__main__:main',
        ],
    },
)