# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compactdata']

package_data = \
{'': ['*']}

install_requires = \
['ply>=3.11,<4.0']

setup_kwargs = {
    'name': 'compactdata',
    'version': '0.0.4',
    'description': 'A parser for the CompactData serialisation format.',
    'long_description': '# CompactData Python Library\n\nA Python library for parsing and serialising data in the CompactData format. CompactData is a compact data serialisation format that prioritises efficiency of data storage and transport. It is well suited for use cases where efficient data storage and transport is a priority.\n\n## Features\n\n- Parse CompactData strings into Python objects\n- Serialise Python objects into CompactData strings\n- Compatible with Python 3.6 and higher\n\n## Installation\n\nTo install the CompactData Python library, use the following command:\n\n```sh\npip install compactdata\n```\n\n## Usage\n\n### Parsing CompactData strings\n\nTo parse a CompactData string into a Python object, use the `compactdata.loads()` function:\n\n```python\nimport compactdata\n\ncompactdata_string = "my_object=(string=`abc`;number=1;array=[1;2;3];map=(a=1;b=2;c=3))"\nparsed_object = compactdata.loads(compactdata_string)\nprint(parsed_object)\n# Output: {\'my_object\': {\'string\': \'abc\', \'number\': 1, \'array\': [1, 2, 3], \'map\': {\'a\': 1, \'b\': 2, \'c\': 3}}}\n```\n\n### Serialising Python objects\n\nTo serialise a Python object into a CompactData string, use the `compactdata.dumps()` function:\n\n```python\nimport compactdata\n\npython_object = {"key1": "value1", "key2": 2}\ncompactdata_string = compactdata.dumps(python_object)\nprint(compactdata_string)\n# Output: (key1=value1;key2=2)\n```\n\n## Examples\n\nHere are some examples of parsing and serialising different CompactData strings and Python objects:\n\n```python\nimport compactdata\n\n# Parsing CompactData strings\ncompactdata_strings = [\n    "my_object=(string=`abc`;number=1;array=[1;2;3];map=(a=1;b=2;c=3))",\n    "[1;2;3]",\n    "a=1;b=2.5;c=10e3",\n    "@dv=1;salts=[(s=salts.domainverification.org;ids=[342c208d-0523-4d22-b7dd-32952dbeace2]);(s=example.com;ids=[90797a69-205b-4a35-88fe-8a186392ea15])]",\n]\n\nfor compactdata_string in compactdata_strings:\n    print(compactdata.loads(compactdata_string))\n    \n# Output:\n# {\'my_object\': {\'string\': \'abc\', \'number\': 1, \'array\': [1, 2, 3], \'map\': {\'a\': 1, \'b\': 2, \'c\': 3}}}\n# [1, 2, 3]\n# {\'a\': 1, \'b\': 2.5, \'c\': 10000.0}\n# {\'@dv\': 1, \'salts\': [{\'s\': \'salts.domainverification.org\', \'ids\': [\'342c208d-0523-4d22-b7dd-32952dbeace2\']}, {\'s\': \'example.com\', \'ids\': [\'90797a69-205b-4a35-88fe-8a186392ea15\']}]}\n\n# Serialising Python objects\npython_objects = [\n    [1, 2, 3, "123"],\n    {"key1": "value1", "key2": 2},\n    "string_value",\n    123,\n    [1, {"k": "v"}, 2],\n]\n\nfor python_object in python_objects:\n    print(compactdata.dumps(python_object))\n\n# Output:\n# [1;2;3;123]\n# (key1=value1;key2=2)\n# string_value\n# 123\n# [1;(k=v);2]\n```\n\n## License\n\nThis project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.\n\n## Support and Contributions\n\nIf you encounter any issues or have feature requests, please [open an issue](https://github.com/NUMtechnology/compactdata-python/issues) on GitHub. Contributions to this project are welcome. To contribute, please fork the repository, make your changes, and submit a pull request.\n\nFor more information about the CompactData format, visit the official website at https://compactdata.org.',
    'author': 'NUM Technology',
    'author_email': 'developer@num.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://compactdata.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
