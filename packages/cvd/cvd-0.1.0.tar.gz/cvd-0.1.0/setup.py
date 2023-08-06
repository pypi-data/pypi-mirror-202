# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvd',
 'cvd.datasets',
 'cvd.datasets.annotations',
 'cvd.datasets.annotations.importer',
 'cvd.datasets.annotations.importer.images',
 'cvd.datasets.annotations.importer.video',
 'cvd.datasets.augumentation',
 'cvd.datasets.autoannotation',
 'cvd.datasets.exporter',
 'cvd.datasets.importer',
 'cvd.datasets.interfaces',
 'cvd.datasets.transformations',
 'cvd.datasets.zoo',
 'cvd.datasets.zoo.raw',
 'cvd.models',
 'cvd.tools',
 'cvd.visualization']

package_data = \
{'': ['*']}

install_requires = \
['albumentations>=1.3.0,<2.0.0',
 'boto3-type-annotations>=0.3.1,<0.4.0',
 'boto3>=1.26.26,<2.0.0',
 'botocore>=1.29.26,<2.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'imagesize>=1.4.1,<2.0.0',
 'lxml>=4.9.1,<5.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'cvd',
    'version': '0.1.0',
    'description': '',
    'long_description': '# datasets\n\n',
    'author': 'bogoslovskiy_nn',
    'author_email': 'bogoslovskiy_nn@bw-sw.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
