# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gqlpycgen']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=5.3.0,<6.0.0',
 'click>=8.1.3,<9.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'requests>=2.28.2,<3.0.0',
 'tenacity>=8.2.2,<9.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['gqlpycgen = gqlpycgencli:cli']}

setup_kwargs = {
    'name': 'wf-gqlpycgen',
    'version': '0.7.4',
    'description': '',
    'long_description': '# gqlpycgen\n\nPython library that generates a python library of a graphql schema.\n',
    'author': 'Paul DeCoursey',
    'author_email': 'paul.decoursey@wildflowerschools.org',
    'maintainer': 'Benjamin Jaffe-Talberg',
    'maintainer_email': 'ben.talberg@wildflowerschools.org',
    'url': 'https://github.com/Wildflowerschools/graphql-python-client-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
