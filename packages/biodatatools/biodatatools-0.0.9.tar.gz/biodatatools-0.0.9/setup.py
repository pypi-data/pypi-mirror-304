from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
	readme = readme_file.read()

requirements = ["genomictools>=0.0.8", "biodata>=0.1.5", "biodataplot>=0.0.4", "simplevc>=0.0.3", "commonhelper>=0.0.5", "mphelper>=0.0.3", "pysam>=0.22.1", "pyBigWig>=0.3.22", "numpy>=1.26.4", "scipy>=1.13.1", "pandas>=2.2.2"]

setup(
	name="biodatatools",
	version="0.0.9",
	author="Alden Leung",
	author_email="alden.leung@gmail.com",
	description="A python package with useful biological data processing methods",
	long_description=readme,
	long_description_content_type="text/markdown",
	url="https://github.com/aldenleung/biodatatools/",
	packages=find_packages(),
	install_requires=requirements,
	classifiers=[
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
	],
	entry_points = {
		'console_scripts': [
			'biodatatools = biodatatools:main',
		],
	}	
)
