# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protopy', 'protopy.bsky']

package_data = \
{'': ['*']}

install_requires = \
['pre-commit>=3.2.2,<4.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'atprotocol',
    'version': '0.0.1',
    'description': 'Python wrapper for the ATProtocol API',
    'long_description': '# atprotocol \n\n🚧 Under construction 🚧\n\nPython wrapper for the [ATProtocol API](https://github.com/bluesky-social/atproto/tree/main/packages/api). It includes:\n- APIs for ATProtocol and Bluesky\n- Validation and (almost) complete Pydantic types\n\n## Getting started\n\n\n\n',
    'author': 'Jett Hollister',
    'author_email': 'jett.hollister@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
