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
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'alwalk0',
    'author_email': 'walkernotwalker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
