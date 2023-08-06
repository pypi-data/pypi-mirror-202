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
    'version': '0.1.3',
    'description': 'A python module to process minion fastq files by concatenating reads as they are generated',
    'long_description': '# Fastq Handler\n\n[![PyPI version](https://badge.fury.io/py/fastq-handler.svg)](https://badge.fury.io/py/fastq-handler)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/fastq-handler.svg)](https://pypi.python.org/pypi/fastq-handler/)\n[![PyPI license](https://img.shields.io/pypi/l/fastq-handler.svg)](https://pypi.python.org/pypi/fastq-handler/)\n[![PyPI status](https://img.shields.io/pypi/status/fastq-handler.svg)](https://pypi.python.org/pypi/fastq-handler/)\n[![PyPI format](https://img.shields.io/pypi/format/fastq-handler.svg)](https://pypi.python.org/pypi/fastq-handler/)\n\nA python module to process ONT fastq files by concatenating reads as they are generated during a sequencing run\n\n## INTRODUCTION\n\nThe _fastqc-handler_ module screens folders and subfolders for fastq (fastq or fastq.gz format) files and concatenates them iteratively. This is useful for merging same-sample reads that are split into multiple files, as commonly obtained in ONT sequencing. The output is a one file per\noutput fastq.gz, containing all reads from the previous files. The output directory structure is maintained.\n\n## INPUT\n\nA directory containing fastq files. The files can be in subfolders (each representing a different sample). The files can be gzipped or not.\n\n## USAGE\n\n```bash\nusage: fastq_handler [-h] [-i INPUT] [-o OUTPUT] [-n TAG] [--keep_names]\n\nparse arguments\n\noptional arguments:\n    -h, --help            show this help message and exit\n    -i INPUT, --input INPUT\n                        Input directory\n    -o OUTPUT, --output OUTPUT\n                        Output directory\n    -n TAG, --tag TAG     Tag to add to output file name\n    --keep_names          Keep original file names in output file\n    --max-size MAX_SIZE   max size of the output file, in kilobytes\n```\n\n## REQUIREMENTS\n\n**Modules**\n\n- dataclasses==0.6\n- natsort==8.3.1\n- pandas==1.5.3\n- setuptools==57.4.0\n- xopen==1.7.0\n\n## INSTALLATION\n\n```bash\npython -m venv .venv\nsource .venv/bin/activate\npython -m pip install fastq-handler\n```\n\n## MAIN OUTPUTS\n\n> **Note:** The output directory structure is maintained.\n\n- **fastq.gz** files containing all reads from the previous files.\n- **log.txt** file containing the concatenation process.\n\n## Maintainers\n\n- [**@xiaodre21**](https://github.com/xiaodre21)\n- [**@santosjgnd**](https://github.com/SantosJGND)\n- [**@insaflu**](https://github.com/insapathogenomics)\n',
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
