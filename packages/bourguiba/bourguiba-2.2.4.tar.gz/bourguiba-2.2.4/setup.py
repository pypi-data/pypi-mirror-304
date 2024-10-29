from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bourguiba",
    version="2.2.4",  # Ensure this is the correct version
    author="si aziz bahloul",
    author_email="azizbahloul3@gmail.com",
    description="sidkom bourguiba ne7elkom il 9mal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AzizBahloul/bourguiba",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'bourguiba': ['ASCII_ART.txt'],  # Include ASCII_ART.txt
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "bourguiba=bourguiba.art:display_ascii_art",
        ],
    },
)
