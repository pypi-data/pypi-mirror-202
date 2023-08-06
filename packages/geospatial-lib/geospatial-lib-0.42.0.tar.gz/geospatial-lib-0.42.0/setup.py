# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geospatial_lib',
 'geospatial_lib.core',
 'geospatial_lib.db',
 'geospatial_lib.misc']

package_data = \
{'': ['*']}

install_requires = \
['GeoAlchemy2>=0.13.1,<0.14.0',
 'SQLAlchemy-Utils>=0.40.0,<0.41.0',
 'SQLAlchemy>=2.0.4,<3.0.0',
 'geopandas>=0.12.2,<0.13.0',
 'psycopg2-binary>=2.9.6,<3.0.0',
 'setuptools>=67.6.1,<68.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'geospatial-lib',
    'version': '0.42.0',
    'description': 'A library with some geo functions',
    'long_description': 'GeoLib\n=====\n[![RunTest](https://github.com/amauryval/geolib/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/amauryval/geolib/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/amauryval/geolib/branch/master/graph/badge.svg)](https://codecov.io/gh/amauryval/geolib)\n\n\n# install\n```bash\npyenv local 3.11.0\npoetry env use 3.11.0\npoetry install\n```',
    'author': 'amauryval',
    'author_email': 'amauryval@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.11.0',
}


setup(**setup_kwargs)
