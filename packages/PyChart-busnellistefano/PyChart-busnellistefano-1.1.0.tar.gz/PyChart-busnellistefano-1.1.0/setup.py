from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name="PyChart-busnellistefano",
  version="1.1.0",
  author="Busnelli Stefano Antonio",
  author_email="busnelli.stefano@gmail.com",
  description="A simple chart class",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://bitbucket.org/StefanoBusnelli/pychart",
  packages=find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3.9",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
  install_requires=["Pillow"],
)
