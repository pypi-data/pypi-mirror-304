from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='IMC_library', # name of packe which will be package dir below project
    version='0.0.1',
    #url='https://github.com/yourname/yourproject',
    author='Gregoire Menard',
    author_email='gregoire.menard.72@hotmail.fr',
    description='library to analyse Imaging Mass Cytometry',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(), #auto_discover packages
    install_requires=[],
)
