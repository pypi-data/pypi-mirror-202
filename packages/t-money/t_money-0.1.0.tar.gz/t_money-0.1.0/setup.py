# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['t_money']
setup_kwargs = {
    'name': 't-money',
    'version': '0.1.0',
    'description': 'Advanced Python 3.10 Dataclass for handling monetary values, keeping amount and currency together',
    'long_description': None,
    'author': 'Jordan Dimov',
    'author_email': 'jdimov@a115.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jordan-dimov/t_money',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
