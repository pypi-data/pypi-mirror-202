# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['clsprop']
setup_kwargs = {
    'name': 'clsprop',
    'version': '1.0.1',
    'description': '🏫 Just like @property but for classes 🏫',
    'long_description': "Works just like @property for classes, except deleters don't work (and are\nperhaps impossible).\n\nInspired by https://stackoverflow.com/a/39542816/43839\n\n## Example\n\n    import clsprop\n\n    class Full:\n        _name = 'fool'\n\n        @clsprop\n        def name(cls):\n            return cls._name\n\n        @name.setter\n        def name(cls, name):\n            cls._name = name\n\n        # Unfortunately, the deleter never gets called\n        @name.deleter\n        def name(cls, name):\n            raise ValueError('Cannot delete name')\n\n    assert Full.name == 'fool'\n\n    Full.name = 'foll'\n    assert Full.name == 'foll'\n\n    del Full.name  # oh, well\n\n\n### [API Documentation](https://rec.github.io/clsprop#clsprop--api-documentation)\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
