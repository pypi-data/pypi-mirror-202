# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easyquery_query_builder']

package_data = \
{'': ['*']}

install_requires = \
['easyvalid-data-validator>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'easyquery-query-builder',
    'version': '0.1.0',
    'description': '',
    'long_description': '## Documentation in development',
    'author': 'Smolke',
    'author_email': 'd.smolczynski1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
