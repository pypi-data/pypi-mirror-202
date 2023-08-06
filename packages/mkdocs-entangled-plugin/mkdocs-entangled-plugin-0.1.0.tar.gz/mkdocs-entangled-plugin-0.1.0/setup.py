# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_entangled']

package_data = \
{'': ['*']}

install_requires = \
['mkdocs>=1.4.2,<2.0.0']

entry_points = \
{'mkdocs.plugins': ['entangled = mkdocs_entangled:EntangledPlugin']}

setup_kwargs = {
    'name': 'mkdocs-entangled-plugin',
    'version': '0.1.0',
    'description': 'Plugin for MkDocs helping with rendering Entangled (entangled.github.io) projects.',
    'long_description': '# Welcome to MkDocs Entangled Plugin\nUsing this plugin, you can make your Entangled documents look better.\n\n## Install\n\nInstall this with `pip install mkdocs-entangled-plugin`. To use the entangled plugin, add the following lines to your `mkdocs.yml`:\n\n```yaml\nplugins:\n  - entangled\n\nmarkdown_extensions:\n  - pymdownx.superfences\n```\n\n## Annotates codeblocks\nThe default markdown syntax that Entangled supports has fenced code blocks as follows\n\n~~~markdown\n ``` {.python file=hello_world.py}\n if __name__ == "__main__":\n     <<hello-world>>\n ```\n~~~\n\nWhich renders like this:\n\n``` {.python file=hello_world.py}\nif __name__ == "__main__":\n    <<hello-world>>\n```\n\nOr named code blocks\n\n~~~markdown\n ``` {.python #hello-world}\n print("Hello, World!")\n ```\n~~~\n\nthat render like this:\n\n``` {.python #hello-world}\nprint("Hello, World!")\n```\n\n## License\nLicensed under the Apache-2 license agreement: see LICENSE\n',
    'author': 'Johan Hidding',
    'author_email': 'j.hidding@esciencecenter.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
