# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fastq_handler']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses==0.6',
 'natsort==8.3.1',
 'pandas==1.5.3',
 'pip==21.2.3',
 'setuptools==57.4.0',
 'xopen==1.7.0']

entry_points = \
{'console_scripts': ['fastq_handler = fastq_handler.__main__:main']}

setup_kwargs = {
    'name': 'fastq-handler',
    'version': '0.1.0',
    'description': 'A python module to process minion fastq files by concatenating reads as they are generated',
    'long_description': None,
    'author': 'SantosJGND',
    'author_email': 'dourado.jns@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
