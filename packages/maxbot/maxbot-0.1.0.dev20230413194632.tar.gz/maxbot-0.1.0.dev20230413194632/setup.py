# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maxbot', 'maxbot.channels', 'maxbot.cli', 'maxbot.extensions', 'maxbot.flows']

package_data = \
{'': ['*']}

install_requires = \
['Babel>=2.12,<3.0',
 'Jinja2>=3.1,<4.0',
 'MarkupSafe>=2.1.2,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'SQLAlchemy>=2.0,<3.0',
 'click>=8.1,<9.0',
 'dateparser>=1.1,<2.0',
 'defusedxml>=0.7.1,<0.8.0',
 'httpx>=0.23,<0.24',
 'markdown-it-py>=2.1.0,<3.0.0',
 'marshmallow>=3.19,<4.0',
 'number-parser>=0.3,<0.4',
 'python-dateutil>=2.8,<3.0',
 'python-dotenv>=1.0,<2.0',
 'python-telegram-bot[ujson]>=20.1,<21.0',
 'pytz>=2022.5,<2023.0',
 'rich>=13.3,<14.0',
 'sanic>=22.12,<23.0',
 'spacy>=3.5,<4.0',
 'textdistance>=4.5,<5.0',
 'tox>=4.4.11,<5.0.0',
 'viberbot>=1.0,<2.0']

entry_points = \
{'console_scripts': ['maxbot = maxbot.cli:main']}

setup_kwargs = {
    'name': 'maxbot',
    'version': '0.1.0.dev20230413194632',
    'description': 'Maxbot is an open source library and framework for creating conversational apps.',
    'long_description': 'None',
    'author': 'Maxbot team',
    'author_email': 'hello@maxbot.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
