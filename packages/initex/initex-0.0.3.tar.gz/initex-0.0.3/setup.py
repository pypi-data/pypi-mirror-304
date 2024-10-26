from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name="initex", # distribution name is required
  version="0.0.3",
  packages=find_packages(),
  description="A package for initializing text files",
  long_description=long_description,
  long_description_content_type="text/markdown"
)