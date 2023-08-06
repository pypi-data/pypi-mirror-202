# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['visioncapsule_tools']

package_data = \
{'': ['*'], 'visioncapsule_tools': ['translations/*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'lxml>=4.6.3,<5.0.0',
 'requests>=2.26.0,<3.0.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['visioncapsule-tools = visioncapsule_tools.cli:cli_main']}

setup_kwargs = {
    'name': 'visioncapsule-tools',
    'version': '0.3.19',
    'description': 'A tool to help users easily download VisionCapsules',
    'long_description': 'None',
    'author': 'Stephen Li',
    'author_email': 'stephen@aotu.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.6.2,<4.0',
}


setup(**setup_kwargs)
