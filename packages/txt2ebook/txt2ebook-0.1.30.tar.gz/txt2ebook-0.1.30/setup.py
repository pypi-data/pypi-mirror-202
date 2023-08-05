# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['txt2ebook',
 'txt2ebook.formats',
 'txt2ebook.formats.templates',
 'txt2ebook.formats.templates.epub',
 'txt2ebook.helpers',
 'txt2ebook.languages',
 'txt2ebook.models']

package_data = \
{'': ['*'],
 'txt2ebook': ['locales/*',
               'locales/en/LC_MESSAGES/txt2ebook.mo',
               'locales/en/LC_MESSAGES/txt2ebook.mo',
               'locales/en/LC_MESSAGES/txt2ebook.po',
               'locales/en/LC_MESSAGES/txt2ebook.po',
               'locales/zh-cn/LC_MESSAGES/txt2ebook.mo',
               'locales/zh-cn/LC_MESSAGES/txt2ebook.mo',
               'locales/zh-cn/LC_MESSAGES/txt2ebook.po',
               'locales/zh-cn/LC_MESSAGES/txt2ebook.po']}

install_requires = \
['CJKwrap>=2.2,<3.0',
 'EbookLib>=0.17.1,<0.18.0',
 'bs4>=0.0.1,<0.0.2',
 'langdetect>=1.0.9,<2.0.0',
 'regex>=2021.11.10,<2022.0.0',
 'tox-pyenv>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['tte = txt2ebook.txt2ebook:main',
                     'txt2ebook = txt2ebook.txt2ebook:main']}

setup_kwargs = {
    'name': 'txt2ebook',
    'version': '0.1.30',
    'description': 'CLI tool to convert txt file to ebook format',
    'long_description': "# txt2ebook\n\nConsole tool to convert txt file to different ebook format.\n\n## Installation\n\nStable version From PyPI:\n\n```console\npython3 -m pip install txt2ebook\n```\n\nLatest development version from GitHub:\n\n```console\npython3 -m pip install -e git+https://github.com/kianmeng/txt2ebook.git\n```\n\n## Usage\n\nShowing help message of command-line options:\n\n```console\ntxt2ebook --help\n```\n\n```console\nusage: txt2ebook [-f {epub,txt}] [-t TITLE] [-l LANGUAGE] [-a AUTHOR]\n                 [-c IMAGE_FILENAME] [-w WIDTH] [-ff FILENAME_FORMAT]\n                 [-ps SEPARATOR] [-rd REGEX] [-rvc REGEX] [-rv REGEX]\n                 [-rc REGEX] [-rt REGEX] [-ra REGEX] [-rl REGEX]\n                 [-rr REGEX REGEX] [-et {clean,noindent,condense}] [-vp] [-tp]\n                 [-sp] [-toc] [-hn] [-fw] [-rw] [-ow] [-v] [-d] [-h] [-V]\n                 TXT_FILENAME [EBOOK_FILENAME]\n\ntxt2ebook/tte is a cli tool to convert txt file to ebook format.\n  website: https://github.com/kianmeng/txt2ebook\n  issues: https://github.com/kianmeng/txt2ebook/issues\n\npositional arguments:\n  TXT_FILENAME\n      source text filename\n  EBOOK_FILENAME\n      converted ebook filename (default: 'TXT_FILENAME.epub')\n\noptional arguments:\n  -f {epub,txt}, --format {epub,txt}\n      ebook format (default: 'epub')\n  -t TITLE, --title TITLE\n      title of the ebook (default: 'None')\n  -l LANGUAGE, --language LANGUAGE\n      language of the ebook (default: 'None')\n  -a AUTHOR, --author AUTHOR\n      author of the ebook (default: '[]')\n  -ff FILENAME_FORMAT, --filename-format FILENAME_FORMAT\n      the output filename format (default: TXT_FILENAME [EBOOK_FILENAME])\n      1 - title_author.EBOOK_EXTENSION\n  -ps SEPARATOR, --paragraph_separator SEPARATOR\n      paragraph separator (default: '\\n\\n')\n  -rd REGEX, --regex-delete REGEX\n      regex to delete word or phrase (default: '[]')\n  -rvc REGEX, --regex-volume-chapter REGEX\n      regex to parse volume and chapter header (default: by LANGUAGE)\n  -rv REGEX, --regex-volume REGEX\n      regex to parse volume header (default: by LANGUAGE)\n  -rc REGEX, --regex-chapter REGEX\n      regex to parse chapter header (default: by LANGUAGE)\n  -rt REGEX, --regex-title REGEX\n      regex to parse title of the book (default: by LANGUAGE)\n  -ra REGEX, --regex-author REGEX\n      regex to parse author of the book (default: by LANGUAGE)\n  -rl REGEX, --regex-delete-line REGEX\n      regex to delete whole line (default: '[]')\n  -rr REGEX REGEX, --regex-replace REGEX REGEX\n      regex to search and replace (default: '[]')\n  -tp, --test-parsing\n      test parsing for volume/chapter header\n  -rw, --raise-on-warning\n      raise exception and stop parsing upon warning\n  -ow, --overwrite\n      overwrite massaged TXT_FILENAME\n  -v, --verbose\n      show verbosity of debugging log, use -vv, -vvv for more details\n  -d, --debug\n      show debugging log and stacktrace\n  -h, --help\n      show this help message and exit\n  -V, --version\n      show program's version number and exit\n\n--format epub:\n  -c IMAGE_FILENAME, --cover IMAGE_FILENAME\n      cover of the ebook\n  -et {clean,noindent,condense}, --epub-template {clean,noindent,condense}\n      CSS template for epub ebook (default: 'clean')\n  -vp, --volume-page\n      generate each volume as separate page\n\n--format txt:\n  -w WIDTH, --width WIDTH\n      width for line wrapping\n  -sp, --split-volume-and-chapter\n      split volume or chapter into separate file and ignore the --overwrite option\n  -toc, --table-of-content\n      add table of content\n\n--language zh-cn / --language zh-tw:\n  -hn, --header-number\n      convert section header from words to numbers\n  -fw, --fullwidth\n      convert ASCII character from halfwidth to fullwidth\n```\n\nConvert a txt file into epub:\n\n```console\ntxt2book ebook.txt\n```\n\n## Copyright and License\n\nCopyright (c) 2021,2022,2023 Kian-Meng Ang\n\nThis program is free software: you can redistribute it and/or modify it under\nthe terms of the GNU Affero General Public License as published by the Free\nSoftware Foundation, either version 3 of the License, or (at your option) any\nlater version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY\nWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A\nPARTICULAR PURPOSE. See the GNU Affero General Public License for more details.\n\nYou should have received a copy of the GNU Affero General Public License along\nwith this program. If not, see <https://www.gnu.org/licenses/>.\n",
    'author': 'Kian-Meng Ang',
    'author_email': 'kianmeng@cpan.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kianmeng/txt2ebook',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
