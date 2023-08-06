# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nanoatp']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'nanoatp',
    'version': '0.1.0',
    'description': 'nano implementation of the AT Protocol (Authenticated Transfer Protocol)',
    'long_description': '# nanoatp\n\nA nano implementation of the AT Protocol (Authenticated Transfer Protocol).\n\n## Getting started\n\nFirst install the package:\n\n```bash\npip install nanoatp\n```\n\nThen in your application:\n\n```python\nfrom nanoatp import BskyAgent\n\nagent = new BskyAgent("https://bsky.social")\n```\n\n## Usage\n\n### Session management\n\nLog into a server using these APIs. You\'ll need an active session for most methods.\n\n```python\nfrom nanoatp import BskyAgent\n\nagent = new BskyAgent("https://bsky.social")\n\nagent.login(\'alice@mail.com\', \'hunter2\')\n\n# if you don\'t specify credentials, ATP_IDENTIFIER and ATP_PASSWORD environment variables will be used\n# agent.login()\n```\n\n### API calls\n\nThe agent includes methods for many common operations, including:\n\n```python\n# Feeds and content\nagent.post(record)\nagent.uploadBlob(data, contentType)\nagent.uploadImage(path, alt, contentType)\n\n# Session management\nagent.login(identifier, password)\n```\n\n## Advanced\n\n### Advanced API calls\n\nThe methods above are convenience wrappers. It covers most but not all available methods.\n\nThe AT Protocol identifies methods and records with reverse-DNS names. You can use them on the agent as well:\n\n```python\nres1 = agent.createRecord(\n    agent.session["did"],  # repo\n    "app.bsky.feed.post",  # collection\n    {\n        "$type": "app.bsky.feed.post",  # record\n        "text": "Hello, world!",\n        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")\n    }\n)\n```\n\n## Development\n\n```bash\nexport ATP_IDENTIFIER="foo.bsky.social"\nexport ATP_PASSWORD="password"\npoetry install\npoetry run pytest -s     # run pytest once\npoetry run -- ptw -- -s  # run pytest and watch for changes\n```\n\n## License\n\nMIT License. See [LICENSE](LICENSE) for details.\n\n## Author\n\nSusumu Ota\n',
    'author': 'Susumu OTA',
    'author_email': '1632335+susumuota@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.16,<4.0.0',
}


setup(**setup_kwargs)
