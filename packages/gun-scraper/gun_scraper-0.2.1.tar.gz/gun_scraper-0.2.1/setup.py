# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gun_scraper', 'gun_scraper.scrapers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['gun_scraper = gun_scraper.__main__:main']}

setup_kwargs = {
    'name': 'gun-scraper',
    'version': '0.2.1',
    'description': 'A simple scraper for finding guns, according to search criteria, from Swedish gun shops',
    'long_description': "# GunScraper\n\nA simple scraper for finding guns, according to search criteria, from Swedish gun shops.\n\nCurrently three shops are supported: \n\n* [Torsbo Handels](https://torsbohandels.com/) \n* [JG Jakt](https://www.jgjakt.se/)\n* [Jaktmarken.se/Marks Jakt och Fiskecenter](https://www.jaktmarken.se)\n\n## Setup\n\nIn order to install and setup GunScraper, follow the steps below:\n\n1. Create a virtual environment\n1. Install GunScraper and dependencies: `pip install gun_scraper`\n1. Download the configuration template `misc/config.yaml`\n1. Update the configuration\n1. Download `misc/runner.sh` and edit it with the path to the virtual environment\n  and config file\n1. Create a Cron Job to run `runner.sh` at desired interval\n\nExample Cron Job, running every 12th hour:\n```\n0 */12 * * * <path-to-repo>/GunScraper/runner.sh >/tmp/stdout.log 2>/tmp/stderr.log\n```\n\n## Config\n\nThe `config.yaml` follows the following syntax:\n\n```yaml\nscraper:\n  filters:\n    # Dictionary defining which filters to apply\n    caliber: # Possible values: 22lr, 22WMR or 308win\n    handedness: # Possible values: left\n  sites:\n    - # List defining which sites to scrape. Supported values: 'torsbo', 'jg' and 'jaktmarken'\n\nemail:\n  sender: # email address that will appear as sender of the notification emails\n  receiver: # email that will receive notification emails\n  smtp_server: # hostname of smtp server used to send notifications\n  ssl_port: # SSL port of the 'smtp_server'\n  username: # username for the 'smtp_server'\n  password: # password for the 'smtp_server'\n  alive_msg_interval: # interval (in hours) to send notification in case no guns matching search criteria is found\n\ndata_folder: # folder to store persistent data in\nlogs_folder: # folder to store log output in\n```",
    'author': 'Erik Persson',
    'author_email': 'erik.ao.persson@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/95ep/GunScraper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
