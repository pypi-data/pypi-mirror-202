# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openvisioncapsule_tools',
 'openvisioncapsule_tools.bulk_accuracy',
 'openvisioncapsule_tools.capsule_benchmark',
 'openvisioncapsule_tools.capsule_classifier_accuracy',
 'openvisioncapsule_tools.capsule_infer',
 'openvisioncapsule_tools.capsule_packaging']

package_data = \
{'': ['*'], 'openvisioncapsule_tools': ['translations/*']}

entry_points = \
{'console_scripts': ['openvisioncapsule-tools = '
                     'openvisioncapsule_tools.cli:cli_main']}

setup_kwargs = {
    'name': 'openvisioncapsule-tools',
    'version': '0.3.7',
    'description': 'A tool to help users to package, test OpenVisionCapsules',
    'long_description': 'None',
    'author': 'Stephen Li',
    'author_email': 'stephen@aotu.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.6.2,<4.0',
}


setup(**setup_kwargs)
