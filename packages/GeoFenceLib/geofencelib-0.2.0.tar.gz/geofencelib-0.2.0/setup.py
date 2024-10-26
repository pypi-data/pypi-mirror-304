# setup.py
from setuptools import setup, find_packages

setup(
    name="GeoFenceLib",
    version="0.2.0",
    packages=find_packages(),
    install_requires=["shapely"],
    author="Abhinav",
    author_email="your.email@example.com",
    description="A Python library for geofencing with dynamic shape and event handling.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)