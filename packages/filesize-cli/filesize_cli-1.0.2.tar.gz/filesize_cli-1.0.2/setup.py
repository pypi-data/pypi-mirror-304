from setuptools import setup, find_packages

setup(
	name='filesize-cli',
	version='1.0.2',
	author='Kolja Nolte',
	author_email='kolja.nolte@gmail.com',
	description='A command-line tool to display the size of a file in various units (B, KB, MB, GB, TB).',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url='https://gitlab.com/thaikolja/filesize-cli',
	packages=find_packages(),
	download_url='https://gitlab.com/thaikolja/filesize-cli/-/archive/main/filesize-cli-main.zip',
	include_package_data=True,
	install_requires=[
		'exceptiongroup==1.2.2',
		'iniconfig==2.0.0',
		'packaging==24.1',
		'pluggy==1.5.0',
		'pytest==8.3.3',
		'setuptools==75.2.0',
		'tomli==2.0.2'
	],
	entry_points={
		'console_scripts': [
			'filesize=filesize_cli.main:main',
		],
	},
	classifiers=[
		'Programming Language :: Python :: 3',
		'Operating System :: OS Independent',
		'License :: OSI Approved :: MIT License',
	],
	python_requires='>=3.6',
)
