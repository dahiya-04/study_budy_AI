from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup( 
    name = "Study_budy",
    version = "0.1.0",
    packages = find_packages(),
    install_requires = requirements,
    description = "A study buddy application to help students manage their study schedules and resources.",
    author = "Sourabh",
)