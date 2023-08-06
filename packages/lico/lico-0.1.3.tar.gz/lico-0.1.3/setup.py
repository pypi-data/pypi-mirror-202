# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lico']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lico',
    'version': '0.1.3',
    'description': 'List processing with csv files',
    'long_description': '# lico\n\n\n[![CI](https://github.com/sjoerdk/lico/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/sjoerdk/lico/actions/workflows/build.yml?query=branch%3Amaster)\n[![PyPI](https://img.shields.io/pypi/v/lico)](https://pypi.org/project/lico/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lico)](https://pypi.org/project/lico/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\nList comb. For quick-and-dirty operations on each row of a csv file.\nHandles boiler-plate code for IO, error handling printing progress. \nOptimized for single-use operations on smaller (< millions) csv files in noisy environments.\n\n## features \n\n* Free software: MIT license\n* Read and write CSV files\n* Run custom operations for each row\n* Handles errors and existing results\n\n## Installation \n\n```\npip install lico\n```\n\n## Usage\n\n### Basic example\n```\nfrom lico.io import Task\nfrom lico.operations import Concatenate\n\n# concatenate column 1 and 2 in input.csv, write to output\nTask(input=\'input.csv\', \n     operation=Concatenate([\'col1\', \'col2\']),\n     output=\'output.csv\').run()\n``` \n\n### Defining operations\n```\nfrom lico.core import Operation\n\n# first of all, subclass lico.core.Operation\nclass MyOperation(Operation):         \n    def apply(self, row):\n        """This method gets called on each row"""\n        old_value = row[\'column1\']           # access values like dict \n        new_value = any_function(old_value)\n        return {\'new_column\': new_value}     # new value(s)\n        # \'new_column\' is appended to existing columns in output\n```\n### Skipping rows\nThere are two ways to tell lico to skip a row.`Operation.has_previous_result()` and raising `RowProcessError`\n```\nfrom lico.core import Operation\nfrom lico.exceptions import RowProcessError\n\nclass MyOperation(Operation):         \n    def apply(self, row):\n        if row[\'col1\'] == \'0\':          \n          raise RowProcessError  # Lico will skip current row   \n        return {\'result\':\'a_result\'}\n        \n    def has_previous_result(self, row):\n      """# If the column \'result\' contains anything, skip this"""      \n      if row.get(\'result\', None):\n        return True   \n      else:\n        return False\n```\n## Built-in error handling\nBeyond skipping lines with previous results or `RowProcessingErrors` there are ways in which lico\nmakes processing more robust:\n\n* Trying to access a non-existent column in Operation.apply() will yield an error and automatically skip that row\n* Output of `Task.run()` will always have the same number of rows as the input. If an unhandled exception occurs during `Task.run()`, lico will stop processing but still write all results obtained\n  so far. The unprocessed rows will be in the output unmodified. \n\n## Logging\nLico uses the root logger `lico`. To print log messages put this in your code:\n```\nimport logging\n\nlogging.basicConfig(level=logging.DEBUG)\n```\n\n## CSV structure\n\nThe idea is to keep CSVs as simple and unambiguous as possible. Therefore:\n\n* All csv values are text. No interpreting things as ints. Too many operations\n  have been messed up by truncating leading zeros etc.\n* csv row headers are required and are considered unique keys\n\n## Why?\n\nSituations in which lico might speed up your work:\n\n* I\'ve got a Here is a csv file of (~1000) rows including `legacy id`\n* Can we find `new id` for each of these legacy ids and also add `datapoint` based on `new id`?\n* We don\'t know whether `legacy id` is valid in all cases. Or at all.\n* This whole procedure is just to \'get an idea\'. Just for exploration\n\nThere are many ways to approach this. Mine is usually to get rid of excel by parsing the data into a flat\ncsv file and then using a combination of a text editor and bash magic for merging, sorting. Intermediate\nsteps are saved for auditing.\n\nHowever, for certain operations such as interacting with servers this is not enough. I then tend to use python.\nThis is more powerful but also creates overhead. Many of these tasks are single-use. Each time I have to slighty\nmodify the same code: read in csv, do something, handle errors, write output.\n\nlico tries to get rid of that boiler plate code as much as possible.\n\n',
    'author': 'sjoerdk',
    'author_email': 'sjoerd.kerkstra@radboudumc.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
