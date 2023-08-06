import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aru",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Shree Aru Bisoi",                     # Full name of the author
    description="All in one mathematical function module",
    long_description="All in one multipurpose mathematical module",      # Long description read from the the readme file
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["aru"],             # Name of the python package
    install_requires=[]                     # Install other dependencies if any
)