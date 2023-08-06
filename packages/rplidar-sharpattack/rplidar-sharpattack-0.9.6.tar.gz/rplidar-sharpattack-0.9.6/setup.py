#!/usr/bin/env python3
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="rplidar-sharpattack",
    py_modules=["rplidar"],
    version="0.9.6",
    description="Simple and lightweight module for working with RPLidar laser scanners",
    author="Artyom Pavlov, Julien Jehl, Arthur Amalvy",
    author_email="arthur.amalvy@univ-avignon.fr",
    url="https://gitlab.com/sharpattack/RPLidar",
    license="MIT",
    install_requires=["pyserial"],
    zip_safe=True,
    long_description="This module aims to implement communication protocol "
    "with RPLidar laser scanners.",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Hardware",
    ],
)
