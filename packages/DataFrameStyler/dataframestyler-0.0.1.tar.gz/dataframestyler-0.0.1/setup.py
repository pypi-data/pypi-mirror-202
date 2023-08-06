import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="DFStyler-SimoneCallegarin", 
    version="0.0.1",
    author="SimoneCallegarin",
    author_email="simone.callegarin@mail.polimi.it",
    description="A dataframe formatting tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SimoneCallegarin/DataframeFormatting/blob/main/Library.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)