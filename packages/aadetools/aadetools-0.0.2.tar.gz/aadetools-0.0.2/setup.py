from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
requirements = [
    'setuptools',
    'pip==19.2.3',
    'bump2version==0.5.11',
    'wheel==0.33.6',
    'watchdog==0.9.0',
    'flake8==3.7.8',
    'tox==3.14.0',
    'coverage==4.5.4',
    'Sphinx==6.1.3',
    'twine==4.0.2',
    'six==1.16.0',
    'farasapy==0.0.14',
    'tqdm==4.62.2',
    'requests==2.25.1',
    'regex==2021.4.4',
    'pickle'
]

setup(
    name="aadetools",                     # This is the name of the package
    version="0.0.2",                        # The initial release version
    url="",                                  #
    author_email="alaa.omer2009@gmail.com",   #
    author="Alaa' Omar",                     # Full name of the author
    description="Test Package Demo",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=find_packages(include=['src.*']),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.9',                # Minimum version requirement of the package
    py_modules=["aadetools"],             # Name of the python package
    install_requires=requirements,         # Install other dependencies if any
    extras_require={
        "Dev":[
            "pytest>=3.7",
        ],
    },
)
