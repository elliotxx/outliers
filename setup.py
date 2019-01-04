#coding=utf8
from setuptools import setup
import outliers

setup(
	name = 'outliers',
	version = '0.1.0',
	keywords = ('outliers', 'detect'),
	description = 'A outliers detect tool.',
	# long_description = 'A outliers detect tool.',
	license = 'MIT licence',

	url = 'https://github.com/elliotxx/outliers',
	author = 'ElliotXX',
	author_email = 'yiyu2017@qq.com',

	py_modules = ['outliers'],

	# include_package_data = True,
	platforms = 'any',
	install_requires = [
		'numpy>=1.14.5',
		'six>=1.5',
		'python-dateutil>=2',
		'pytz>=2011k',
		'pandas>=0.22.0',
		'SciPy>= 0.13.3',
		'scikit-learn>=0.19.2',
	],

	entry_points = {
		'console_scripts' : [
			'outliers = outliers:main'
		]
	}
)