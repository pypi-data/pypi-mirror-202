# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_hell_auth']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.5,<5.0.0',
 'pre-commit>=3.2.2,<4.0.0',
 'requests>=2.28.2,<3.0.0',
 'types-requests>=2.28.11.17,<3.0.0.0']

setup_kwargs = {
    'name': 'django-hell-auth',
    'version': '0.0.3',
    'description': 'hell gitlab auth for django',
    'long_description': '# Django App for HellAuth\n\n\n![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/alte-hoelle/django-hell-auth/main.yml)\n![PyPI](https://img.shields.io/pypi/v/django-hell-auth)\n\n\nThis is a simple Django Auth App for our django tools.  \n\n## pre-commit hooks\n\n### run\n\n```shell\npre-commit run --all-files  \n```\n\n### install\n\n```shell\npre-commit install\n```\n',
    'author': 'David Bauer',
    'author_email': 'hausprojekt@debauer.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
