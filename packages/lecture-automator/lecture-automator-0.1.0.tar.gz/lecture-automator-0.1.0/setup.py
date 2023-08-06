# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lecture_automator']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'numpy>=1.24.2,<2.0.0',
 'torch>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['lecture-automator = '
                     'lecture_automator.cli:convert_md_to_mp4']}

setup_kwargs = {
    'name': 'lecture-automator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'CapBlood',
    'author_email': 'stalker.anonim@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
