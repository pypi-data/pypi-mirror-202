# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atprotocol', 'atprotocol.bsky']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.7,<2.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'atprotocol',
    'version': '0.0.2',
    'description': 'Python wrapper for the ATProtocol API',
    'long_description': "# atprotocol \n\n🚧 Under construction 🚧\n\nPython 3.10 wrapper for the [ATProtocol API](https://github.com/bluesky-social/atproto/tree/main/packages/api). It aims to closely emulate the Typescript implementation, including:\n- APIs for ATProtocol and Bluesky\n- Validation and (almost) complete types\n\n## Getting started\n\nFirst install the package:\n\n```shell\npip install atprotocol\n```\n\nThen in your application:\n\n```python\nfrom atprotocol.bsky import BskyAgent\n\nagent = BskyAgent()\n```\n\n## Usage\n\n### Session management\nLog into a server using these APIs. You'll need an active session for most methods.\n\n```python\nfrom atprotocol.bsky import BskyAgent\n\nagent = BskyAgent()\nagent.login(identifier='jett.ai', password='letsgoduke')\n```\n\n### API calls\n\nThese are the calls currently available in `atprotocol`. More are being added regularly.\n\n```python\n# Feeds and content\nagent.get_timeline()\nagent.get_author_feed(actor, limit)\nagent.get_post_thread(uri, depth)\nagent.get_likes(uri, cid, limit)\nagent.get_reposted_by(uri, cid, limit)\n\n# Social graph\nagent.get_followers(actor)\n\n# Actors\nagent.get_profile(actor)\nagent.get_profiles(actors)\nagent.search_actors(term, limit)\n\n# Session management\nagent.login(params)\n```\n\n## Advanced\n\n### Generic agent\n\nIf you want a generic AT Protocol agent without methods related to the Bluesky social lexicon, use the AtpAgent instead of the BskyAgent.\n\n```python\nfrom atprotocol import AtpAgent\n\nagent = AtpAgent(service='https://example.com')\n```\n\n\n## License\nMIT",
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
