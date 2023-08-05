# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['midi_point_set']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=3.1.0,<4.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'pretty_midi>=0.2.10,<0.3.0']

entry_points = \
{'console_scripts': ['midi-point-set = midi_point_set.console:main']}

setup_kwargs = {
    'name': 'midi-point-set',
    'version': '0.1.0',
    'description': 'Convert MIDI files to point set representation.',
    'long_description': '# MIDI to Point Set Converter\n\nThis Python library converts MIDI files to point set representation, which\nencodes notes as pairs of integers encoding the pitch and time. The output can\nbe used for machine learning tasks such as music generation.\n\n## Requirements\n\n- Python 3.7 or higher\n\n## Installation\n\n```sh\npip install midi_point_set\n```\n\n## Usage\n\n### CLI\n\n```sh\n# JSON output\n\npython -m midi-point-set --input-midi K545-1.mid --output-json mozart.json\n\n# Plot\n# (requires matplotlib installed)\npython -m midi-point-set --input-midi K545-1.mid --output-plot mozart.svg\n```\n\n### Library\n\n```py\nfrom midi_point_set import get_point_set\n\npoint_set = get_point_set("mozart.midi")\nprint(point_set[:5])\n```\n',
    'author': 'Leo',
    'author_email': 'leohdz.c0@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
