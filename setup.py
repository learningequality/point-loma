# from setuptools import setup

# setup( 
# 	name='HelloWorld',
# 	version='1.0',
# 	py_modules=['hello'],
# 	install_requires=[
# 		'Click',
# 	],
# 	entry_points='''
# 		[console_scripts]
# 		hello=hello:cli
# 	''',
# )

from setuptools import setup

setup(
	name='pointLoma',
	version='0.2',
	py_modules=['pointLoma', 'sh', 'parselighthouse'],
	install_requires=[
		'sh', 'Click', 'pathlib'
	],
	entry_points='''
		[console_scripts]
		pointloma=pointLoma:cli
	''',
)