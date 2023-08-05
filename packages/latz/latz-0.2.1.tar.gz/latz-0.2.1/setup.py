# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latz',
 'latz.commands',
 'latz.commands.config',
 'latz.config',
 'latz.plugins',
 'latz.plugins.image']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'click>=8.1.3,<9.0.0',
 'httpx>=0.23.1,<0.24.0',
 'pluggy>=1.0.0,<2.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'rich-click>=1.6.0,<2.0.0',
 'rich>=13.3.3,<14.0.0']

entry_points = \
{'console_scripts': ['latz = latz.cli:cli']}

setup_kwargs = {
    'name': 'latz',
    'version': '0.2.1',
    'description': 'CLI Program for downloading images. Maybe by location too...',
    'long_description': '# Overview\n\n[pluggy]: https://pluggy.readthedocs.io/en/stable/\n[click]: https://click.palletsprojects.com/\n[pydantic]: https://docs.pydantic.dev/\n[rich]: https://rich.readthedocs.io/\n[anaconda.org]: https://anaconda.org\n[latz-imgur]: https://github.com/travishathaway/latz-imgur\n[creating-plugins]: creating-plugins\n\nThis is a command line tool used for retrieving images from various image\nsearch backends (e.g. Unsplash, Google). This tool is primarily developed for educational purposes\nto show people how to develop plugin friendly Python applications. Furthermore,\nit is an example project that shows how to effectively pair a handful of\npopular Python libraries to write command line applications.\n\nTo facilitate our plugin architecture, the [pluggy][pluggy] library is used.\nOther libraries used include the following:\n\n- [click][click]: used for structuring the command line application 🖱 💻\n- [pydantic][pydantic]: used for handling configuration file validation 🗃\n- [rich][rich]: used for UX/UI elements and generally making the application more pretty 🌈\n\n### Why "latz"\n\n"latz" is short and easy to type! This is super important when writing CLI programs.\nI also might add a geolocation search feature, so it is a reference  to the word "latitude".\n\n## Quick Start\n\n### Installation\n\nlatz is available for install either on PyPI:\n\n```bash\n# Run from a new virtual environment\n$ pip install latz\n```\n\nor my own [anaconda.org][anaconda.org] channel:\n\n```bash\n$ conda create -n latz \'thath::latz\'\n```\n\nIf you are interested in tinkering around with the code yourself, you can also\nrun it locally:\n\n```bash\n$ git clone git@github.com:/travishathaway/latz.git\n$ cd latz\n# Create a virtual environment however you like..\n$ pip install -e .\n```\n\n### Usage\n\nLatz comes initially configured with the "unsplash" image search backend. To use this,\nyou will need to create an Unsplash account and create a test application. After getting\nyour "access_key", you can set this value by running this command:\n\n```bash\n$ latz config set search_backend_settings.unsplash.access_key=<YOUR_ACCESS_KEY>\n```\n\nOnce this is configured, you can search Unsplash for bunny pictures:\n\n```bash\n$ latz search "bunny"\n[\n    ImageSearchResultSet(\n        results=(\n            ImageSearchResult(\n                url=\'https://unsplash.com/photos/u_kMWN-BWyU/download?ixid=MnwzOTMwOTR8MHwxfHNlYXJjaHwxfHxidW5ueXxlbnwwfHx8fDE2Nzk0MTA2NzQ\',\n                width=3456,\n                height=5184\n            ),\n            # ... results truncated\n        ),\n        total_number_results=10,\n        search_backend=\'unsplash\'\n    )\n]\n```\n\n### Configuring\n\nThe configuration for latz is stored in your home direct and is in the JSON format.\nBelow is a what a default version of this configuration looks like:\n\n```json\n{\n  "search_backends": [\n    "unsplash"\n  ],\n  "search_backend_settings": {\n    "placeholder": {\n      "type": "kitten"\n    },\n    "unsplash": {\n      "access_key": "your-access-key"\n    }\n  }\n}\n```\n\n_Latz will also search in your current working directory for a `.latz.json` file and use this in your configuration.\nFiles in the current working directory will be prioritized over your home directory location._\n\nTo see other available image search backends, see [Available image search backends](#available-image-search-backends) below.\n\n### Available image search backends\n\nHere are a list of the available search backends:\n\n#### Built-in\n\n- "unsplash"\n- "placeholder"\n\n#### Third-party\n\n- [latz-imgur][latz-imgur]\n\n### How to extend and write your own image search backend\n\nPlease see the [creating plugins][creating-plugins] guide in the documentation.\n',
    'author': 'Travis Hathaway',
    'author_email': 'travis.j.hathaway@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
