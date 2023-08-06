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
    'version': '0.2.2',
    'description': 'Basic utilities for PyBullet, including collision detection, ghost (i.e. visual-only) objects, and cameras.',
    'long_description': "# pyb_utils: utilities for PyBullet\n\nThis is a collection of utilities I've found useful for working with PyBullet,\nincluding:\n* Collision detection: conveniently set up shortest distance computations and\n  collision checking between arbitrary objects in arbitrary configurations with\n  PyBullet. See the accompanying [blog post](https://adamheins.com/blog/collision-detection-pybullet).\n* Ghost objects: add purely visual objects to the simulation, optionally\n  attached to another body.\n* Camera: virtual camera from which to get RGBA, depth, segmentation, and point\n  cloud data. Also provides video recording using OpenCV.\n\n## Install and run\nThis package requires **Python 3.7+**. It has been tested on Ubuntu 16.04,\n18.04, and 20.04.\n\n### From source\nClone the repo:\n```bash\ngit clone https://github.com/adamheins/pyb_utils\ncd pyb_utils\n```\n\nInstall using [poetry](https://python-poetry.org/):\n```bash\npoetry install\npoetry run python scripts/collision_detection_example.py  # for example\n```\n\nOr using pip:\n```bash\npython -m pip install .\n```\n\n### Directly from GitHub\n```\npython -m pip install git+https://github.com/adamheins/pyb_utils\n```\n\n## Usage and examples\nYou can find example scripts demonstrating all of this package's utilities in\nthe `scripts/` directory:\n\n* [collision detection](https://github.com/adamheins/pyb_utils/blob/main/scripts/collision_detection_example.py)\n* [ghost objects](https://github.com/adamheins/pyb_utils/blob/main/scripts/ghost_object_example.py)\n* [camera](https://github.com/adamheins/pyb_utils/blob/main/scripts/camera_example.py)\n* [video](https://github.com/adamheins/pyb_utils/blob/main/scripts/video_example.py)\n\n## Known issues\nFeel free to open issues (or better yet, a pull request!) if you find a\nproblem. Currently known issues:\n\n* Video recording does not output MP4 videos correctly. The AVI format works,\n  however.\n* Ghost objects sometimes flicker (spooky, but undesirable).\n\n## License\n[MIT](https://github.com/adamheins/pyb_utils/blob/main/LICENSE)\n",
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
