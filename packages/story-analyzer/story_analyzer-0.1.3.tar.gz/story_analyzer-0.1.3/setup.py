# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['story_analyzer', 'story_analyzer.tests']

package_data = \
{'': ['*'], 'story_analyzer': ['data/*']}

install_requires = \
['beautifulsoup4>=4.12.2,<5.0.0',
 'colorama>=0.4.6,<0.5.0',
 'gensim>=4.3.1,<5.0.0',
 'sentencepiece>=0.1.97,<0.2.0',
 'sortedcontainers>=2.4.0,<3.0.0',
 'spacy>=3.5.1,<4.0.0',
 'torch>=2.0.0,<3.0.0',
 'transformers>=4.27.4,<5.0.0']

entry_points = \
{'console_scripts': ['story_analyzer = story_analyzer.main:main']}

setup_kwargs = {
    'name': 'story-analyzer',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Story Analyzer\n\nGet all the details of a story. From summaries to character information, explore your book like never before!\n\n![Banner](banner.jpg)\n\n## Features\n\n* Quiz game\n* Translation \n* Summarization  \n* Most relevant topics\n* Characteres list \n* Lines list\n* Number of sentences\n* Match of input phrase with a storie excert\n\n## Usage\n\n```\nusage: main.py [-h] [-m {local,web}] [-q] [-t [{English,Spanish,French,German,Italian,Portuguese}]] [-d] [-s] [-l] [-c] [-a [ACTIONS]]\n               [--save title] [-p PROJECTION]\n               input output\n\nBook Analyzer: get insight informations of your storie\n\npositional arguments:\n  input                 input file path or book name (only in web mode)\n  output                output file path\n\noptions:\n  -h, --help            show this help message and exit\n  -m {local,web}, --mode {local,web}\n                        app modes\n  -q, --quiz            quiz game\n  -t [{English,Spanish,French,German,Italian,Portuguese}], --translate [{English,Spanish,French,German,Italian,Portuguese}]\n                        translate the book\n  -d, --discussions     list the book discussions (topics)\n  -s, --summary         summarize the book\n  -l, --language        detect book language\n  -c, --characters      get informations of the book characters\n  -a [ACTIONS], --actions [ACTIONS]\n                        get the top most actions of a book\n  --save title          the book will be saved and so will any queries invoked deemed savable.\n  -p PROJECTION, --projection PROJECTION\n                        project queries in the text range. Projection type is [<bottom>;<higher>]\n  -sa, --sentiment-analysis\n                        get the sentiment analysis of the book\n```\n\n## Dependencies\n\n* Quiz game is made with https://huggingface.co/gpt2\n* Transaltion is made with https://huggingface.co/docs/transformers/main/en/model_doc/t5#overview\n* Summarization is made with https://huggingface.co/docs/transformers/model_doc/pegasus\n* Most Relevent Topics is made with https://radimrehurek.com/gensim/\n* Language detection is made with https://huggingface.co/papluca/xlm-roberta-base-language-detection\n* Actions, Characters and places list is made with https://spacy.io/\n* HTML extraction is made with https://www.crummy.com/software/BeautifulSoup/bs4/doc/',
    'author': 'Francisco Alexandre Neves',
    'author_email': 'pg50375@alunos.uminho.pt',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
