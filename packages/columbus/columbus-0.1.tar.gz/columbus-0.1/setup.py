# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['columbus', 'columbus.framework']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'alembic>=1.9.3,<2.0.0',
 'asyncpg>=0.27.0,<0.28.0',
 'databases>=0.7.0,<0.8.0',
 'psycopg2>=2.9.5,<3.0.0',
 'pyaml>=21.10.1,<22.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'starlette>=0.24.0,<0.25.0',
 'typer>=0.7.0,<0.8.0',
 'uvicorn>=0.20.0,<0.21.0',
 'watchfiles>=0.18.1,<0.19.0']

entry_points = \
{'console_scripts': ['run = columbus.run:app', 'start = columbus.start:app']}

setup_kwargs = {
    'name': 'columbus',
    'version': '0.1',
    'description': 'Generate an async web API from an SQLAlchemy table',
    'long_description': "# Columbus\n\n![PyPI](https://img.shields.io/pypi/v/columbus)\n\n\n\n### What is Columbus?\n\nColumbus is a Python web framework that automatically generates an async CRUD REST API web application from an SQLAlchemy table.\n\n### How does it work?\n\nUnder the hood Columbus uses [Starlette](https://www.starlette.io), [Databases](https://pypi.org/project/databases/) and [SQLAlchemy](https://www.sqlalchemy.org) along with some interesting metaprogramming techniques to generate a web app based solely on your YAML specification and SQLalchemy table definition. \n\n### Installation\n\n ```pip install columbus```\n\n### Quickstart\n\nYou can have your API up and running in only a couple of simple steps:\n\n1. ```start```\n\n\tThis command will generate two files for you:\n\tmain.yml with a basic config template and an empty models.py.\n\n2. **In models.py define your database table using SQLAlchemy.** <br><br>\n\tThen create the tables ([Alembic](https://alembic.sqlalchemy.org/en/latest/) is generally the recommended way to do this) and add some data whichever way you like. Columbus doesn't need you to connect to the database or write any queries for the app to work, it will do that for you. All you need to do is provide it with the database url.\n\n3. **In main.yml add the database url** as a value for the 'database' key. **Add the name of your table** as the value for the 'table' key. <br><br>Here is a basic working example (provided you've set up the database with this url and your table is named my_table and located in models.py).\n\n\t```\n\tmodels: models.py\n\tdatabase: postgresql://someuser:postgres@localhost/mydatabase\n\tAPIs:\n\t  hello_world:\n\t    table: my_table\n\t    methods: [GET]\n\t```    \n\t\n\n\n4. ```run```\n\n\tThis command will run your app. **Navigate to localhost:8000/my_table and see your API in action**.\n\t\n\t\n### Documentation\n\nHere is a comprehensive list of possible keys and values in the YAML config.\n\nKeys:\n\n- **models**: relative path to the file where your SQLAlchemy table is defined\n\n\n- **database**: valid database url\n\n- **APIs**: the APIs you want Columbus to generate. Each API can be named whatever you want, but it has two mandatory keys:\n\t\n\t- **table**: name of SQLAlchemy table from which you want to generate the API\n\t\n\t-  **methods**: list of http methods (GET, PUT, POST, DELETE) you want the API to support. Attention: this is the only key that needs to be a list, so put the methods in square brackets.\n\nBelow is an example of a more comprehensive animals API, which should give you a feel for the correct YAML structure Columbus understands. Incorrect structures will throw an error and the app won't run.\n\n\n```\nmodels: models.py\ndatabase: postgresql://someuser:postgres@localhost/mydatabase\nAPIs:\n  dogs:\n    table: dogs\n    methods: [GET, POST]\n  cats:\n    table: cats   \n    methods: [GET, POST, PUT, DELETE] \n  snakes:\n    table: snakes\n    methods: [GET, POST, PUT]   \n  bears:\n    table: bears\n    methods: [GET]    \n```    \n    \n    \n    \n    \n    \n    \n### What use cases does it support?\n\nColumbus is still in the early days of active development, so it only supports the most basic use case for now. Feel free to open an issue for a missing feature and it will most likely be pushed to the top of the priority list and shipped soon.\n            \n\n\n\n\n\t\n\t\n\t\n",
    'author': 'alwalk0',
    'author_email': 'walkernotwalker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leftfile/columbus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
