# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chromat']

package_data = \
{'': ['*']}

install_requires = \
['colour>=0.1.5,<0.2.0', 'textual>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'chromat',
    'version': '0.0.3',
    'description': 'color palettes! under heavy construction!',
    'long_description': '\ufeff# chromat: algorithmic color palettes\ncoming soon!\n\nhttps://github.com/hexbenjamin/chromat',
    'author': 'hex benjamin',
    'author_email': 'hex@hexbenjam.in',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hexbenjamin/chromat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
