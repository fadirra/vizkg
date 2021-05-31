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
with codecs.open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='VizKG',
    packages=['VizKG', 'VizKG.charts', 'VizKG.utils'],
    version='0.0.0.1',
    description='Visualization library for SPARQL query results',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Hana',
    install_requires=install_reqs,
    license='MIT',
)