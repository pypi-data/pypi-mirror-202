# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_core',
 'polywrap_core.types',
 'polywrap_core.types.options',
 'polywrap_core.utils']

package_data = \
{'': ['*']}

install_requires = \
['polywrap-manifest==0.1.0a15', 'polywrap-msgpack==0.1.0a15']

setup_kwargs = {
    'name': 'polywrap-core',
    'version': '0.1.0a15',
    'description': '',
    'long_description': 'None',
    'author': 'Cesar',
    'author_email': 'cesar@polywrap.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
