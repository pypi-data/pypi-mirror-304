
from setuptools import setup, find_packages

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

#get version
with open(path.join(this_directory, 'VERSION'), encoding='utf-8') as f:
    version = f.read()

# TODO add domutils to tests_requires when it is made available on conda-forge
setup(
    name='domcmc',
    version=version,
    url='https://gitlab.science.gc.ca/dja001/domcmc',
    license='MIT',
    license_files=('LICENSE.txt',),
    author='Dominik Jacques',
    author_email='dominik.jacques@gmail.com',
    description="dominik's tools for reading fst files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),    
    python_requires='>=3', 
    install_requires=['numpy'],
    tests_require=['doctest', 'matplotlib', 'cartopy', 'sphinx', 'sphinx-autodoc-typehints', 
                   'sphinx-gallery', 'sphinx_rtd_theme', 'cartopy'] 
)
