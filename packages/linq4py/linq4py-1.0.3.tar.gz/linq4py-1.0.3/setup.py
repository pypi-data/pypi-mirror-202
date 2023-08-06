# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linq4py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'linq4py',
    'version': '1.0.3',
    'description': 'Linq for python',
    'long_description': '# Linq for Python\n\n像C#或JavaScript一样链式写python\n\n## 1 代码说明\n代码Fork `https://pypi.org/project/py-linq/`\n\n## 2 新增功能\n- 新增：`filter`,`map`,`find`等类似于JavaScript`filter`,`map`,`find`\n- 使用函数式入口来初始化列表`linq4py.array()`\n\n## 3 举例\n\n```\nimport linq4py as lp\n\norigin_items = [\n    {\'id\': \'1\', \'parent_id\': \'\', \'name\': \'indicator 1\', \'weight\': 1, \'has_child\': True},\n    {\'id\': \'2\', \'parent_id\': \'1\', \'name\': \'indicator 2\', \'weight\': 0.6, \'has_child\': True},\n    {\'id\': \'3\', \'parent_id\': \'1\', \'name\': \'indicator 3\', \'weight\': 0.4, \'has_child\': True},\n    {\'id\': \'4\', \'parent_id\': \'2\', \'name\': \'indicator 4\', \'weight\': 0.5, \'has_child\': False},\n    {\'id\': \'5\', \'parent_id\': \'2\', \'name\': \'indicator 5\', \'weight\': 0.8, \'has_child\': False},\n    {\'id\': \'6\', \'parent_id\': \'3\', \'name\': \'indicator 6\', \'weight\': 0.8, \'has_child\': False},\n    {\'id\': \'7\', \'parent_id\': \'3\', \'name\': \'indicator 7\', \'weight\': 0.8, \'has_child\': False},\n]\n\n\n# count demo\ncount = lp.array(origin_items).count(lambda item: item[\'has_child\'])\nprint(count)\n\n# filter,order_by_descending map demo\nitems = lp.array(origin_items).filter(lambda item: item["has_child"]).order_by_descending(\n    lambda item: item[\'weight\']).map(lambda item: (item[\'id\'], item[\'name\']))\nprint(items)\n\n# find demo\nresult = lp.array(origin_items).find(lambda item: item[\'weight\'] > 0.3)\nprint(result)\n\n```\n\n## 4 修改日志\n\n- 2023-04-08 重新打包\n- 2023-04-08 Fork项目并新增相关功能',
    'author': 'six006',
    'author_email': 'six006@126.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
