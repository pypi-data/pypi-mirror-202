# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['origen', 'origen.ai']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'origen-ai-ecl',
    'version': '0.1.3',
    'description': '',
    'long_description': '# opm-origen\n\n## Prerequisites\n\n- Install make, cmake and g++\n- Build/Install Opm-Common\n- Build/Install Opm-Grid\n\n## Install opm packages\n\n```bash\nsudo apt-add-repository ppa:opm/ppa\nsudo apt-get update\n\nsudo apt-get install libopm-common-dev\nsudo apt-get install libopm-grid-dev\n```\n\n## How to build\n\n```bash\ngit clone git@github.com:OriGenAI/opm-origen.git\ncd opm-origen\nmkdir build\ncd build\ncmake ..\nmake\n```\n\n## How to use\n\n- Copy the binary under `build/lib` folder\n- Import the binary from your Python code\n- Call the library functions\n\n## Example\n\n```python\nfrom origen.ai.ecl import read_transmissibility\n\ntrans = read_transmissibility("path-to-data.DATA")\nprint(trans)\n```\n\n## Develop\n\nYou can use the main.cpp file to debug. Just call your function from there and compile the code. You will find the binary in `build/bin/main`\n',
    'author': 'Luis Arce',
    'author_email': 'luis@origen.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
