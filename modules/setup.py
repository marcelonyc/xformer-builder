from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Validate python code with RestrictedPython"
LONG_DESCRIPTION = ""

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="python_modules",
    version=0.1,
    author="Marcelo Litovsky",
    author_email="marcelo@litovsky.com",
    description="Modules used in api and Dashboard",
    packages=find_packages(),
    install_requires=[
        "RestrictedPython==8.0"
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=["python", "code", "validator", "transformer"],
    classifiers=[
        "Development Status :: 1 - Prod",
        "Intended Audience :: Open Source Developers",
        "Programming Language :: Python :: 3",
    ],
)
