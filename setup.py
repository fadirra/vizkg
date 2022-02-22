import codecs
import os
import re
from setuptools import find_packages, setup

def local_file(file):
  return codecs.open(
    os.path.join(os.path.dirname(__file__), file), 'r', 'utf-8'
)

install_reqs = [
  line.strip()
  for line in local_file('requirements.txt').readlines()
  if line.strip() != ''
]

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='VizKG',
    packages=['VizKG', 'VizKG.charts', 'VizKG.utils'],
    version='1.0.9',
    description='Visualization library for SPARQL query results',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls = {
    "Source Code": "https://github.com/fadirra/vizkg",
    "Demo" : "https://www.youtube.com/watch?v=i0dd_-PRxlI"
    },
    author='Hana',
    install_requires=install_reqs,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7'
)