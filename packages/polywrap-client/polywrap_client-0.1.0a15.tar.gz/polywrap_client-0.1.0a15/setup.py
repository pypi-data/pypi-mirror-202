# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polywrap_client']

package_data = \
{'': ['*']}

install_requires = \
['polywrap-core>=0.1.0a15,<0.2.0',
 'polywrap-manifest>=0.1.0a15,<0.2.0',
 'polywrap-msgpack>=0.1.0a15,<0.2.0',
 'polywrap-uri-resolvers>=0.1.0a15,<0.2.0']

setup_kwargs = {
    'name': 'polywrap-client',
    'version': '0.1.0a15',
    'description': '',
    'long_description': '# polywrap-client\n\nPython implementation of the polywrap client.\n\n## Usage\n\n### Configure and Instantiate\n\nUse the `polywrap-uri-resolvers` package to configure resolver and build config for the client.\n\n```python\nfrom polywrap_uri_resolvers import FsUriResolver, SimpleFileReader\n\nconfig = ClientConfig(\n    resolver=FsUriResolver(file_reader=SimpleFileReader())\n)\n\nclient = PolywrapClient(config)\n```\n\n### Invoke\n\nInvoke a wrapper.\n\n```python\nuri = Uri.from_str(\n    \'fs/<path to wrapper>\'  # Example uses simple math wrapper\n)\nargs = {\n    "arg1": "123",  # The base number\n    "obj": {\n        "prop1": "1000",  # multiply the base number by this factor\n    },\n}\noptions: InvokerOptions[UriPackageOrWrapper] = InvokerOptions(\n    uri=uri, method="method", args=args, encode_result=False\n)\nresult = await client.invoke(options)\nassert result == "123000"\n```',
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
