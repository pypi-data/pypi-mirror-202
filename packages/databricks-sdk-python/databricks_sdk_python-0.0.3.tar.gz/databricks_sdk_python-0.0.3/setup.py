# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databricks_sdk_python',
 'databricks_sdk_python.api_client',
 'databricks_sdk_python.api_client.account',
 'databricks_sdk_python.api_client.account.aws',
 'databricks_sdk_python.api_client.workspace',
 'databricks_sdk_python.api_client.workspace.unity_catalog',
 'databricks_sdk_python.resources',
 'databricks_sdk_python.resources.account',
 'databricks_sdk_python.resources.account.aws',
 'databricks_sdk_python.resources.workspace',
 'databricks_sdk_python.resources.workspace.unity_catalog']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.4.0,<2.0.0', 'requests>=2.22']

setup_kwargs = {
    'name': 'databricks-sdk-python',
    'version': '0.0.3',
    'description': 'Objet based databricks sdk',
    'long_description': '[![PyPI version](https://badge.fury.io/py/databricks-sdk-python.svg)](https://badge.fury.io/py/databricks-sdk-python)\n[![codecov](https://codecov.io/github/ffinfo/databricks-sdk-python/branch/main/graph/badge.svg?token=EOJDSTI5KN)](https://codecov.io/github/ffinfo/databricks-sdk-python)\n[![Python package](https://github.com/ffinfo/databricks-sdk-python/actions/workflows/python-package.yml/badge.svg)](https://github.com/ffinfo/databricks-sdk-python/actions/workflows/python-package.yml)\n\n# databricks-sdk-python\n\n### Install\n\n```bash\npip install databricks-sdk-python\n```\n\n\n### Install for developers\n\n###### Install package\n\n- Requirement: Poetry 1.*\n\n```shell\npoetry install\n```\n\n###### Run unit tests\n```shell\npytest\ncoverage run -m pytest  # with coverage\n# or (depends on your local env) \npoetry run pytest\npoetry run coverage run -m pytest  # with coverage\n```\n\n##### Run linting\n\nThe linting is checked in the github workflow. To fix and review issues run this:\n```shell\nblack .   # Auto fix all issues\nisort .   # Auto fix all issues\npflake .  # Only display issues, fixing is manual\n```\n',
    'author': "Peter van 't Hof'",
    'author_email': 'peter.vanthof@godatadriven.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffinfo/databricks-sdk-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
