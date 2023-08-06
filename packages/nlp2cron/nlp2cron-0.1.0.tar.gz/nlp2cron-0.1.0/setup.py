# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nlp2cron']
install_requires = \
['cn2an>=0.5.19,<0.6.0']

setup_kwargs = {
    'name': 'nlp2cron',
    'version': '0.1.0',
    'description': 'Nature language to cron',
    'long_description': '## 中文自然语言转CRON\n\n为了支持一次性任务, 我在cron表达式后面加了个标志位, \nT 代表是频率任务, F 代表是一次性任务\n\n如果没这个需要,直接去掉最后一位就可以啦\n',
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
