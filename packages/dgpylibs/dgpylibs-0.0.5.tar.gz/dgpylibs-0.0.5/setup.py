# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['dgpylibs', 'dgpylibs.dev']

package_data = \
{'': ['*']}

install_requires = \
['aiopen',
 'asyncify',
 'fmts',
 'funkify',
 'h5>=0.8.8',
 'jsonbourne',
 'lager>=0.17.0',
 'listless',
 'requires',
 'shellfish',
 'xtyping']

setup_kwargs = {
    'name': 'dgpylibs',
    'version': '0.0.5',
    'description': 'Dynamic Graphics Python libraries',
    'long_description': 'None',
    'author': 'jessekrubin',
    'author_email': 'jesse@dgi.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
