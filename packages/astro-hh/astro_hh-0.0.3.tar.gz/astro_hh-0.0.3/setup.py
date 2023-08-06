import setuptools
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="astro_hh",
  version="0.0.3",
  author="HuangHao",
  author_email="ironlionwg@outlook.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/pypa/sampleproject",
  packages=find_packages(".\\"),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
