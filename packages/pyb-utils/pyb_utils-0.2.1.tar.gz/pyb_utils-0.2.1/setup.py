# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyb_utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.21.5,<2.0.0',
 'opencv-python>=4.5.5,<5.0.0',
 'pybullet>=3.2.1,<4.0.0',
 'spatialmath-python>=1.0.0']

setup_kwargs = {
    'name': 'pyb-utils',
    'version': '0.2.1',
    'description': 'Basic utilities for PyBullet, including collision detection, ghost (i.e. visual-only) objects, and cameras.',
    'long_description': 'None',
    'author': 'Adam Heins',
    'author_email': 'mail@adamheins.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
