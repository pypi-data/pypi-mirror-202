# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cbrzn_ethereum_provider_py', 'cbrzn_ethereum_provider_py.wrap']

package_data = \
{'': ['*']}

install_requires = \
['eth_account==0.8.0', 'polywrap-plugin==0.1.0a28', 'web3==6.1.0']

setup_kwargs = {
    'name': 'cbrzn-ethereum-provider-py',
    'version': '0.0.2',
    'description': 'Ethereum provider in python',
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
