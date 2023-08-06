from setuptools import setup, find_packages
from lorettOrbital import __version__


with open("requirements.txt", 'r') as file:
      requirements =  file.readlines()
 
with open("README.md", "r") as fh:
	long_description = fh.read()

setup(name='lorettOrbital',
      version=__version__,
      url='https://gitlab.com/lpmrfentazis/lorettorbital',
      license='MIT',
      author='MrFentazis',
      author_email='lpmrfentazis@mail.ru',
      description='LorettOrbital Python 3 library for orbital calculations and planning',
      long_description=long_description,
      packages=find_packages(),
      install_requires=requirements,
      test_suite="tests",
      classifiers=[
		"Programming Language :: Python :: 3.9",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
      python_requires='>=3.9'
      )