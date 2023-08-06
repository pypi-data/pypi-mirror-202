import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zopperuuid", # Name of your pacakage
    version="0.0.5", # Version of your pacakage
    author="Saurav Sharma",
    author_email="saurav.sharma@zopper.com",
    description="This Package will help in generating the UUID",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.zopper.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # install_requires=['requests'], # Mention dependent libraries/packages for building your package
)