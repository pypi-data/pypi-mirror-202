# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_client_config_builder',
 'polywrap_client_config_builder.configures',
 'polywrap_client_config_builder.types']

package_data = \
{'': ['*']}

install_requires = \
['polywrap-core>=0.1.0a15,<0.2.0', 'polywrap-uri-resolvers>=0.1.0a15,<0.2.0']

setup_kwargs = {
    'name': 'polywrap-client-config-builder',
    'version': '0.1.0a15',
    'description': '',
    'long_description': '# polywrap-client-config-builder\n\nA utility class for building the PolywrapClient config. \n\nSupports building configs using method chaining or imperatively.\n\n## Quickstart\n\n### Initialize\n\nInitialize a ClientConfigBuilder using the constructor\n\n```python\n# start with a blank slate (typical usage)\nbuilder = ClientConfigBuilder()\n```\n\n### Configure\n\nAdd client configuration with add, or flexibly mix and match builder configuration methods to add and remove configuration items.\n\n```python\n# add multiple items to the configuration using the catch-all `add` method\nbuilder.add(\n    BuilderConfig(\n        envs={},\n        interfaces={},\n        redirects={},\n        wrappers={},\n        packages={},\n        resolvers=[]\n    )\n)\n\n// add or remove items by chaining method calls\nbuilder\n    .add_package("wrap://plugin/package", test_plugin({}))\n    .remove_package("wrap://plugin/package")\n    .add_packages(\n      {\n        "wrap://plugin/http": http_plugin({}),\n        "wrap://plugin/filesystem": file_system_plugin({}),\n      }\n    )\n```\n\n### Build\n\nFinally, build a ClientConfig to pass to the PolywrapClient constructor.\n\n```python\n# accepted by the PolywrapClient\nconfig = builder.build()\n\n# build with a custom cache\nconfig = builder.build({\n  wrapperCache: WrapperCache(),\n})\n\n# or build with a custom resolver\ncoreClientConfig = builder.build({\n  resolver: RecursiveResolver(...),\n})\n```\n',
    'author': 'Media',
    'author_email': 'media@polywrap.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
