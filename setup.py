from setuptools import setup

setup(
	name='pointLoma',
	version='0.2',
	py_modules=['pointLoma', 'sh', 'path'],
	install_requires=[
		'sh', 'Click', 'pathlib'
	],
	entry_points='''
		[console_scripts]
		pointloma=pointLoma:cli
	''',
)