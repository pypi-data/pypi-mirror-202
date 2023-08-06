# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tidy3d_lambda']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tidy3d-lambda',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Kidy Lee',
    'author_email': 'kidylee@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
