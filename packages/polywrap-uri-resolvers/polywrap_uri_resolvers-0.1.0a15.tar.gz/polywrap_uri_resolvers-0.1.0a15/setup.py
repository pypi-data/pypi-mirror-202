# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_uri_resolvers',
 'polywrap_uri_resolvers.resolvers',
 'polywrap_uri_resolvers.resolvers.abc',
 'polywrap_uri_resolvers.resolvers.aggregator',
 'polywrap_uri_resolvers.resolvers.cache',
 'polywrap_uri_resolvers.resolvers.extensions',
 'polywrap_uri_resolvers.resolvers.legacy',
 'polywrap_uri_resolvers.resolvers.package',
 'polywrap_uri_resolvers.resolvers.recursive',
 'polywrap_uri_resolvers.resolvers.redirect',
 'polywrap_uri_resolvers.resolvers.static',
 'polywrap_uri_resolvers.resolvers.wrapper',
 'polywrap_uri_resolvers.types',
 'polywrap_uri_resolvers.types.cache',
 'polywrap_uri_resolvers.types.uri_resolution_context',
 'polywrap_uri_resolvers.utils']

package_data = \
{'': ['*']}

install_requires = \
['polywrap-core==0.1.0a15', 'polywrap-wasm==0.1.0a15']

setup_kwargs = {
    'name': 'polywrap-uri-resolvers',
    'version': '0.1.0a15',
    'description': '',
    'long_description': '# polywrap-uri-resolvers\n\nURI resolvers to customize URI resolution in the Polywrap Client.\n\n',
    'author': 'Cesar',
    'author_email': 'cesar@polywrap.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
