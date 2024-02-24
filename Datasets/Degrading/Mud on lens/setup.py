from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

__version__ = "0.0.0"
with open("ivs/sensors/__init__.py") as f:
    exec(f.read())  # loads the correct version in __version__

setup(
    name="ivs-sensors",
    version=__version__,
    author="Gabriele Baris",
    author_email="gabriele.baris@warwick.ac.uk",
    description="Python library for sensors modelling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://wmg-gitlab.wmgds.wmg.warwick.ac.uk/iv-sensors/phd/gabri/ivs-sensors-python",
    project_urls={
        "Bug Tracker": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: None",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=["ivs.sensors.*"]),
    python_requires=">=3.6",
    install_requires=required,
)
