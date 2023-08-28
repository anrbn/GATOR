from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the version from the VERSION file
with open("VERSION", "r") as v:
    version = v.read().strip()

# Read requirements from the requirements.txt
with open("requirements.txt", "r", encoding="utf-16") as f:
    requirements = f.read().splitlines()

setup(
    name="gator-red",
    version=version,
    packages=find_packages(),
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'gator=gator.main:main',
        ],
    },
    package_data={
        '': ['VERSION'],  # Include VERSION file
    },
    include_package_data=True,  # Include package data
)
