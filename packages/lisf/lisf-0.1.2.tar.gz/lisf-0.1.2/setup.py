# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lisf']
install_requires = \
['asgiref>=3.6.0,<4.0.0']

setup_kwargs = {
    'name': 'lisf',
    'version': '0.1.2',
    'description': 'Lazy Instantiated Singleton Factory',
    'long_description': 'None',
    'author': 'imi',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
