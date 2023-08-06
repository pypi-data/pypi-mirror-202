# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brainframe_sys_tools', 'brainframe_sys_tools.brainframe_monitor']

package_data = \
{'': ['*'], 'brainframe_sys_tools': ['translations/*']}

install_requires = \
['brainframe-api>=0.29.1,<0.30.0']

entry_points = \
{'console_scripts': ['brainframe-sys-tools = '
                     'brainframe_sys_tools.cli:cli_main']}

setup_kwargs = {
    'name': 'brainframe-sys-tools',
    'version': '0.3.19',
    'description': 'This is the package including tools for BrainFrame developers to monitor and debug the system.',
    'long_description': 'None',
    'author': 'Stephen Li',
    'author_email': 'stephen@aotu.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<4.0',
}


setup(**setup_kwargs)
