from setuptools import setup, find_packages

setup(
    name="pyJStrobe",      # Replace with your package name
    version="0.1",                 # Version number
    packages=find_packages(),      # Automatically find and include all packages
    author="Joseph Louis",
    author_email="joseph.louis@oregonstate.edu",
    description="This package is used to automate the DES application jStrobe.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',       # Specify minimum Python version (optional)
)
