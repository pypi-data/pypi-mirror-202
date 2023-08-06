# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_invest',
 'python_invest.cli',
 'python_invest.cli.commands',
 'python_invest.invest']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0',
 'pandas>=1.5.3,<2.0.0',
 'rich>=13.3.3,<14.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pinv = python_invest.cli:cli']}

setup_kwargs = {
    'name': 'python-invest',
    'version': '0.2.1a0',
    'description': 'Package to financial data extraction with Python.',
    'long_description': '# Python Invest\n\n![Python Invest Logo](./docs/images/logo.png "Python Invest Logo")\n\nFinancial data extraction with Python.\n\nThe Python Invest package is based on an unofficial data extraction API from the website [Investing.com](https://www.investing.com/). It\'s a package inspired by the amazing [Investpy](https://github.com/alvarobartt/investpy) library.\n\n<i>:warning:</i><b> This package consumes an unofficial open API and will validate the user\'s email before providing the data. After that, the user can consume all available services.</b>\n\nPython Invest its a Open Source package and Free to use, respecting the **MIT License**.\n\n## :book: Documentation\n\nThe oficial [Documentation](https://pyinvest.readthedocs.io/en/latest/).\n\n## :material-list-status: Requirements\n\n:white_check_mark: Python >= 3.10\n\n## :hammer_and_wrench: Installation\n\n- pip\n\n```\n$ pip install python-invest\n```\n\n- poetry\n\n```\npoetry add python-invest\n```\n\n---\n\n## :chart_with_upwards_trend: Usage Examples\n\nGetting historical **BTC** data:\n\n```{.py3 linenums=1 hl_lines=5}\nfrom python_invest import Invest\n\ninv = Invest(\'youremail@email.com\')\n\ndata = inv.crypto.get_historical_data(\n        symbol=\'BTC\',\n        from_date=\'2023-01-01\',\n        to_date=\'2023-02-01\'\n    )\n```\n\nThe API can send a verification link to your email, it\'s a security measure you won\'t be charged for anything. If this happens, you will receive an error similar to this:\n\n```{hl_lines="3 5"}\nTraceback (most recent call last):\n File "...", line 5, in <module>\n    data = inv.crypto.get_historical_data(symbol=\'BTC\', from_date=\'2023-01-01\', to_date=\'2023-02-01\')\n    ...\nPermissionError: The Scrapper API sent to your email address the verification link. Please verify your email before run the code again.\n```\n\nIf you get this error: **Just open your email box and click on the verification link.**\n\nThe email would be a equal this:\n\n![Verification Email Link](./docs/images/emailValidation.png "Verification Email Link")\n\nAfter that, you can run the code:\n\n```{.py3 linenums=5}\ndata = inv.crypto.get_historical_data(\n        symbol=\'BTC\',\n        from_date=\'2023-01-01\',\n        to_date=\'2023-02-01\'\n    )\n\nprint(data)\n```\n```\n      Price      Open      High       Low     Vol Change        Date\n0  16,674.3  16,618.4  16,766.9  16,551.0  136027   0.34  01/02/2023\n1  16,618.4  16,537.5  16,621.9  16,499.7  107837   0.49  01/01/2023\n```\n\nThe default output is the [Pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).\n\n## :keyboard: CLI\n\n```bash\npinv --help\n```\n\n---\n\n**Example**:\n\n```bash\npinv crypto historical BTC --date-in \'2023-01-01\' --date-out \'2023-04-01\' --time-frame \'Monthly\'\n```\n```\n                            TABLE OF HISTORICAL DATA\n┏━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓\n┃ Price    ┃ Open     ┃ High     ┃ Low      ┃ Vol     ┃ Change ┃ Date       ┃\n┡━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩\n│ 23,130.5 │ 23,124.7 │ 25,236.8 │ 21,418.7 │ 9094707 │ 0.02   │ 02/01/2023 │\n│ 23,125.1 │ 16,537.5 │ 23,952.9 │ 16,499.7 │ 8976036 │ 39.83  │ 01/01/2023 │\n└──────────┴──────────┴──────────┴──────────┴─────────┴────────┴────────────┘\n```\n\n## :computer: Social Medias\n* [Instagram](https://www.instagram.com/claudiogfez/)\n* [Linkedin](https://www.linkedin.com/in/clcostaf/)\n\n# :technologist: Author\n| [<img src="https://avatars.githubusercontent.com/u/83929403?v=4" width=120><br><sub>@clcostaf</sub>](https://github.com/clcosta) |\n| :---: |\n',
    'author': 'Claudio Lima',
    'author_email': 'clcostaf@hotmail.com',
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
