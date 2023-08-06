# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdsite']

package_data = \
{'': ['*'],
 'mdsite': ['testdata/*', 'testdata/conflict/*', 'testdata/nougat/*']}

install_requires = \
['MarkupSafe>=2.1.2,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'markdown2>=2.4.8,<3.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'markdown-site-utils',
    'version': '0.2.1',
    'description': 'Some utilities for managing Markdown files with metadata.',
    'long_description': '# Markdown Site Utils\n\nSome utilities for managing Markdown files with metadata.\n\nThe notion is that a content-oriented website may be written as a \nhierarchical series of Markdown files (with an ".md" extension) underneath\nsome data directory, e.g.:\n\n    DATA_DIR/\n      index.md\n      foo.md\n      bar.md\n      subdir/\n        index.md\n        foo.md\n        bar.md\n\nEach file may contain metadata, written in TOML in a section at\nthe top, bounded by \'+++\' lines:\n\n    +++\n    title = "My Page Title"\n    +++\n\n    # Some Markdown\n\nYAML and JSON may also be used. YAML blocks should start and end with lines\nconsisting of three dashes; JSON blocks should consist of a single JSON object\nwith opening and closing braces on lines by themselves. The data block is optional\nbut if present must begin on the first line of the file.\n\nTo use the library, you get create an `mdsite.DB` object with the path to your\ndata directory:\n\n    mydb = mdsite.DB("/path/to/data/dir")\n\nThen call `get_data(path)` for the path into the directory you want, leaving\nout the `.md` filename suffix, and, if you are looking for an index file, leaving\nout `index.md`:\n\n    data = mydb.get_data("/node/leaf")\n\nThe above gets data for `$DATA_DIR/node/leaf.md`, or for\n`$DATA_DIR/node/leaf/index.md`, if that file exists instead. \n\nThe library also supports hierarchical configuration, also written in TOML,\nYAML, or JSON, stored in files called `config.{toml,yaml,json}` depending on the\nconfig language employed.\n',
    'author': 'Jacob Smullyan',
    'author_email': 'smulloni@smullyan.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/smulloni/markdown_site_utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
