# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['try_except_ai']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.4,<0.28.0']

setup_kwargs = {
    'name': 'try-except-ai',
    'version': '0.1.0',
    'description': 'A Python package to handle exceptions and suggest resolutions using OpenAI',
    'long_description': '# TryExceptAI\n\nA Python package to handle exceptions and suggest resolutions using OpenAI.\n\n## Installation\n\nInstall the package using [Poetry](https://python-poetry.org/):\n\n```bash\npoetry add try-except-ai\n```\n\n## Usage\n```python\nfrom try_except_ai import TryExceptAI\n\ndef test_function():\n    try:\n        # Code that might raise an exception\n        result = 1 / 0\n        print(result)\n    except Exception as e:\n        TryExceptAI().handle_exception(e)\n\nif __name__ == "__main__":\n    test_function()\n\n```\n\n## License\nThis project is licensed under the MIT License. See the LICENSE file for details.\n\n',
    'author': 'Federico Ulfo',
    'author_email': 'federicoulfo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etnalab/try-except-ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
