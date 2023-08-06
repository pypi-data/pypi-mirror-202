# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nlp2cron']
install_requires = \
['cn2an>=0.5.19,<0.6.0']

setup_kwargs = {
    'name': 'nlp2cron',
    'version': '0.1.3',
    'description': 'Nature language to cron',
    'long_description': '## 中文自然语言转CRON\n\npip install nlp2cron\n\n```python\nfrom nlp2cron import nlp2cron\ncron = nlp2cron("每天10点25分叫我去买菜")\n\n```\n\n你会得到一个`cron`表达式. 目前代码写的有点乱, 但只要不太随意的自然语言都可以解决\n代码里面有一些例子, 详细看代码啦. 代码写的比较随意, 如果要求高请不要用啦.\n\n',
    'author': 'quqinglei',
    'author_email': 'quqinglei@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
