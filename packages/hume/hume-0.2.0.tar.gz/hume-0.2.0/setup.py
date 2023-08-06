# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hume',
 'hume._batch',
 'hume._common',
 'hume._stream',
 'hume.error',
 'hume.models',
 'hume.models.config']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'typing-extensions>=4.3.0,<5.0.0']

extras_require = \
{'stream': ['websockets>=10.3,<11.0']}

setup_kwargs = {
    'name': 'hume',
    'version': '0.2.0',
    'description': 'Hume AI Python Client',
    'long_description': '<div align="center">\n  <img src="https://storage.googleapis.com/hume-public-logos/hume/hume-banner.png">\n  <h1>Hume AI Python SDK</h1>\n\n  <p>\n    <strong>Integrate Hume APIs directly into your Python application</strong>\n  </p>\n\n  <br>\n  <div>\n    <a href="https://humeai.github.io/hume-python-sdk"><img src="https://img.shields.io/badge/docs-mkdocs-blue" alt="Docs"></a>\n    <a href="https://pepy.tech/project/hume"><img src="https://pepy.tech/badge/hume" alt="Downloads"></a>\n    <a href="https://pypi.org/project/hume"><img src="https://img.shields.io/pypi/v/hume?logo=python&logoColor=%23cccccc" alt="PyPI"></a>\n    <a href="https://github.com/HumeAI/hume-python-sdk/actions/workflows/ci.yml"><img src="https://github.com/HumeAI/hume-python-sdk/actions/workflows/ci.yaml/badge.svg" alt="CI"></a>\n  </div>\n  <br>\n</div>\n\nTo get started, [sign up for a Hume account](https://share.hsforms.com/1lVY-gpw0RTaWCeu7ZTkH-wcjsur)!\n\n> We\'re in private beta right now, but we\'ll be continuously rolling out access to developers and organizations on our waitlist.\n\n## Usage & Documentation\n\nFor usage examples check out the [full documentation](https://humeai.github.io/hume-python-sdk/).\n\n## Other Resources\n\n- [Hume AI Homepage](https://hume.ai)\n- [Platform Documentation](https://help.hume.ai/basics/about-hume-ai)\n- [API Reference](https://docs.hume.ai)\n\n## Citations\n\nHume\'s expressive communication platform has been built on top of published scientific research. If you use this SDK in your work please see [CITATIONS.md](CITATIONS.md) for the best way to reference that research.\n\n## Support\n\nIf you\'ve found a bug with this SDK please [open an issue](https://github.com/HumeAI/hume-python-sdk/issues/new)!\n',
    'author': 'Hume AI Dev',
    'author_email': 'dev@hume.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/HumeAI/hume-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<4',
}


setup(**setup_kwargs)
