# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fringes_gui']

package_data = \
{'': ['*']}

install_requires = \
['fringes>=0.1.5,<0.2.0',
 'opencv-contrib-python>=4.7.0,<5.0.0',
 'pyqt6>=6.4.2,<7.0.0',
 'pyqtgraph>=0.13.2,<0.14.0',
 'pyyaml>=6.0,<7.0',
 'scikit-image>=0.19.3,<0.20.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'fringes-gui',
    'version': '0.1.1',
    'description': "Graphical user interface for the 'fringes' package.",
    'long_description': "# Fringes-GUI\nAuthor: Christian Kludt\n\n## Description\nGraphical user interface for the [fringes](https://pypi.org/project/fringes/) package.\n\n## Installation\nYou can install `fringes-gui` directly from [PyPi](https://pypi.org/project/fringes-gui) via `pip`:\n\n```\npip install fringes-gui\n```\n\n## Usage\nYou import the `fringes-gui` package and call the function `run()`.\n\n```python\nimport fringes_gui as fgui\nfgui.run()\n```\n\nNow the graphical user interface should appear:\n\n![Screenshot](docs/GUI.png)\\\nScreenshot of the GUI.\n\n### Parameter Tree\nIn the top left corner the attribute widget is located.\nIt contains the parameter tree with which all the properties of the `Fringes` class\nfrom the [fringes](https://pypi.org/project/fringes/) package can be controlled.\nCheck out its website for more details.\nHowever, if you select a parameter and hover over it, a tool tip will appear\ncontaining the docstring of the respective property of the `Fringes` class.\n\nThe Visibility defines the type of user that should get access to the feature.\nIt does not affect the functionality of the features but is used by the GUI to\ndecide which features to display based on the current user level. The purpose\nis mainly to ensure that the GUI is not cluttered with information that is not\nintended at the current visibility level. The following criteria have been used\nfor the assignment of the recommended visibility:\n- Beginner: Features that should be visible for all users via the GUI. This\nis the default visibility. The number of features with 'Beginner' visibility\nshould be limited to all basic features so the GUI display is well-organized\nand easy to use.\n- Expert: Features that require a more in-depth knowledge of the system\nfunctionality. This is the preferred visibility level for all advanced features.\n- Guru: Advanced features that usually only people with a sound background in phase shifting can make good use of.\n- Experimental: New features that have not been tested yet\nand the system might probably crash at some point.\n\n### Function Buttons\nIn the bottem left corner you will find buttons for the associated methods of the `Fringes` class.\nAlternatively, you can use the keyboard shortcuts which are displayed when you hover over the buttons.\nThe buttons are only active if the necessary data has been enoded, decoded or loaded.\n\n### Viewer\nIn the center resides the viewer.\nIf float data is to be displayed, nan is replaced by zeros.\n\n### Data\nIn the top right corner the data widget is located.\nIt lists the data which has been encoded, decoded or was loaded.\n\nIn order to keep the [Parameter Tree](#parameter-tree) consistent with the data,\nonce a parameter has changed, certain data will be removed\nand also certain [buttons](#function-buttons) will be deactivated.\nAs a consequence, if you load data - e.g. the acquired (deflected) fringe pattern sequence - \nthe first element of its videoshape has to match the parameter `Frames` in order to be able to decode it.\n\nTo display any datum listed in the table in the [Viewer](#viewer), simly select the name of it in the table.\n\nKlick the `Load` button to choose a data or parameter set to load.\nWith the `Save` button, all data including the parameter set are saved to the selected directory.\nUse the `Clear all` button to delete all data.\n\nPlease note: By default, the datum `fringes` is decoded.\nIf you want to decode a datum with a different name (e.g. one that you just loaded),\nselect its name in the table and klick `Set data (to be decoded)`.\n\n### Log\nHere the logging of the `Fringes` class is displayed.\nThe logging level can be set in the [Parameter Tree](#parameter-tree).\n\n## License\nCreative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License\n",
    'author': 'Christian Kludt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/comimag/fringes-gui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
