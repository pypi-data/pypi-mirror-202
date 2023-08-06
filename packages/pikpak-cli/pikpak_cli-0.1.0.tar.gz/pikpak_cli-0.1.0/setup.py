# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pikpak_cli']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.3.1',
 'ant-nest>=1.0.1',
 'ipython>=8.11.0',
 'prompt-toolkit>=3.0.38',
 'rich>=13.3.1',
 'tenacity>=4.8.0',
 'tqdm>=4.64.1',
 'typer>=0.7.0',
 'typing_extensions>=3.6',
 'ujson>=1.3.4']

entry_points = \
{'console_scripts': ['pikpak_cli = pikpak_cli.main:main']}

setup_kwargs = {
    'name': 'pikpak-cli',
    'version': '0.1.0',
    'description': 'A pikpak command line client',
    'long_description': "CLI for Pikpak(A web file driver)\n\n# Features\n\n* List all file in a tree\n* Download a whole folder\n* Download files by file name or size matching\n* Download resume(which will create a .part file before finished)\n\n# Install\n\n```shell\npip install -U pikpak_cli\n```\n\n# Usage\n\n```\npikpak_cli\nCurrent account: ******\nDefault download dir: ****\nsession file: .pikpak.session\ntry typing help\npikpak_cli>help\nlogin\nLogin account\nusage: login [-h] [--password PASSWORD] account [account ...]\n\nexit\nExit cli\nusage: exit [-h]\n\nshell\n\nusage: shell [-h]\n\nls\nList current dir files\nusage: ls [-h] [--without_audit] [--trash] [--recursion] name [name ...]\n\ncd\nChange directory\nusage: cd [-h] name [name ...]\n\ndownload\nDownload a file or many files in a directory\nusage: download [-h] [--includes INCLUDES] [--excludes EXCLUDES] [--dir DIR] [--size SIZE] [--relative_path] [--new_file_name NEW_FILE_NAME] name [name ...]\n\npwd\nGet current path\nusage: pwd [-h]\n\ndu\nGet files's total size\nusage: du [-h] name [name ...]\n\nhelp\nGet help information\nusage: help [-h]\n\nconfig\nSet default download dir or\nusage: config [-h] [--downlaod_dir DOWNLAOD_DIR]\n\ninfo\nPrint session info\nusage: info [-h]\n\nrm\n\nusage: rm [-h] [--no_trash] name [name ...]\n```\n\ntry `help`!\n\n## examples\n\n### ls\n\n```shell\npikpak_cli>ls .\n```\n\ntry `--recursion`!\n\n### cd\n\n```shell\npikpak_cli>cd Movie\npikpak_cli>pwd\npikpak_cli>/Movie\n```\n\n```shell\npikpak_cli>cd ..\npikpak_cli>\n```\n\n### download\n\ndownload files only bigger than 500M to `/mnt` with a flat structure:\n\n```shell\npikpak_cli>download Movie --size 500M --relative_path --dir /mnt\n```\n\ndownload all mp4 or mkv files to default download dir:\n\n```shell\npikpak_cli>download Movie --includes *.mp4,*.mkv\n```\n",
    'author': 'strongbugman',
    'author_email': 'strongbugman@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/strongbugman/pikpak_cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
