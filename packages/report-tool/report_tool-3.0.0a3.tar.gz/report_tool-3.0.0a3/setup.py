# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['report_tool',
 'report_tool.calculate',
 'report_tool.communications',
 'report_tool.exports',
 'report_tool.logger',
 'report_tool.qt',
 'report_tool.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.9,<6.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'pyqtgraph>=0.13.2,<0.14.0',
 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['report-tool = report_tool.__main__:main']}

setup_kwargs = {
    'name': 'report-tool',
    'version': '3.0.0a3',
    'description': 'Report Tool is an application that uses IG Rest API to show basic statistics about past trades.',
    'long_description': '# Report Tool 3.0.0-alpha3\n\n[![Latest GitHub release][latest-release]][latest-release-url]\n![Latest GitHub pre-release][latest-prerelease]\n\nReport Tool is an application coded in Python 3.11 / PyQt5 using IG Rest API to show basics statistics about past trades.\n\n## Features\n\n* Listing of past trades,\n* Summary in points, points per lot, currency or percentage\n* Equity curves,\n* Export of trades in .txt format or .jpeg format\n* Trades comment,\n* Market filter.\n\n![Main interface][gui-main-window]\n\n## Installation\n\n### What you will need\n\n* Python 3.11: https://www.python.org/downloads/\n* pip (should already be installed with Python): https://pip.pypa.io/en/stable/installing/\n* poetry: `curl -sSL https://install.python-poetry.org | python3 -`\n  * More info: https://python-poetry.org/docs/#installing-with-the-official-installer\n\n### Dependencies\n\n```shell script\ncd Report-Tool\npoetry install\n```\n\n## Usage\n\n* Download the archive and unzip it:\n* Either run the entry point:\n```shell script\ncd Report-Tool\npoetry run report-tool\n```\n* Or run the script:\n```shell script\ncd Report-Tool\npoetry run python -m report_tool\n```\n* Enter your credentials, via the menu "Connect"\n\n![Connect menu][gui-connect-menu]\n\n* Have fun !\n\n## Building the msi installer\n\n```shell script\ncd Report-Tool\npoetry run python setup.py bdist_msi\n```\n\n## Disclaimer\n\nThis tool was originally created by user **beniSo**, but he\'s no longer on GitHub.\n\n\n[latest-prerelease]: https://img.shields.io/github/v/release/Mulugruntz/Report-Tool?include_prereleases&label=Report%20Tool\n[latest-release]: https://img.shields.io/github/v/release/Mulugruntz/Report-Tool?label=Report%20Tool\n[latest-release-url]: https://github.com/Mulugruntz/Report-Tool/releases/latest\n\n[gui-main-window]: https://github.com/Mulugruntz/Report-Tool/raw/master/docs/main.png\n[gui-connect-menu]: https://github.com/Mulugruntz/Report-Tool/raw/master/docs/connect.png\n',
    'author': 'Samuel Giffard',
    'author_email': 'samuel@giffard.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Mulugruntz/Report-Tool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
