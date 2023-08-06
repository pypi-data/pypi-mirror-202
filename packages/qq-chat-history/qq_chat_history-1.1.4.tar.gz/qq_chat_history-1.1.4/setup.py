# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qq_chat_history']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pyyaml>=6.0,<7.0', 'ujson>=5.7.0,<6.0.0']

entry_points = \
{'console_scripts': ['qq-chat-history = qq_chat_history.cli:run']}

setup_kwargs = {
    'name': 'qq-chat-history',
    'version': '1.1.4',
    'description': 'A tool to extract QQ chat history.',
    'long_description': "# QQ 聊天记录提取器\n\n## 简介\n\n从 QQ 聊天记录文件中提取聊天信息，仅支持 `txt` 格式的聊天记录。\n\n\n## 安装\n\n使用 `pip` 安装，要求 `Python 3.9` 或以上版本。\n\n```bash\n> pip install -U qq-chat-history\n```\n\n## 使用\n\n最简单的启动方式如下，它会自动在当前目录下创建 `output.json` 进行输出（如果安装到虚拟环境请确保已激活）。\n\n```bash\n> qq-chat-history /path/to/file.txt\n```\n\n启动时输入 `--help` 参数查看更多配置项。\n\n```bash\n> qq-chat-history --help\n```\n\n或者，可以作为一个第三方库使用，如下：\n\n```python\nimport qq_chat_history\n\nlines = '''\n=========\n假装我是 QQ 自动生成的文件头\n=========\n\n1883-03-07 11:22:33 A<someone@example.com>\n关注永雏塔菲喵\n关注永雏塔菲谢谢喵\n\n1883-03-07 12:34:56 B(123123)\nTCG\n\n1883-03-07 13:24:36 C(456456)\nTCG\n\n1883-03-07 22:00:51 A<someone@example.com>\n塔菲怎么你了\n'''.strip().splitlines()\n\n# 这里的 lines 也可以是文件对象或者以字符串或者 Path 对象表示的文件路径。\nfor msg in qq_chat_history.parse(lines):\n    print(msg.date, msg.id, msg.name, msg.content)\n```\n\n注意 `parse` 方法返回的是一个 `Body` 对象，一般以 `Iterable[Message]` 的形式使用。当然 `Body` 也提供了几个函数，~虽然一般也没什么用~。\n\n## Tips\n\n+ 在 `0.3.0+` 版本中，对于 `parse` 方法的实现进行了较大调整，它将返回一个 `Body` 类，原先是 `Iterable[Message]`。但这并**不会导致兼容性问题**，因为 `Body` 也是一个 `Iterable[Message]`。\n\n  不同的是，`Body` 类相对于原先单纯的生成器**提供更多功能**，例如`find_xxx` 方法，可以从数据中查找指定 `id` 或 `name` 的消息；`save` 方法可以将数据以 `yaml` 或 `json` 格式保存到文件中，虽然这个工作一般都直接以 `CLI` 模式启动来完成。\n\n+ 在 `0.3.0+` 版本中，你可以向 `parse` 中传入多样的类型。\n\n  + `Iterable[str]`：迭代每行的可迭代对象，如 `list` 或 `tuple` 等。\n  + `TextIOBase`：文本文件对象，如用 `open` 打开的文本文件，或者 `io.StringIO` 都属于文本文件对象。\n  + `str`, `Path`：文件路径，如 `./data.txt`。\n\n  这些参数都将以对应的方法来构造 `Body` 对象。\n",
    'author': 'kifuan',
    'author_email': 'kifuan@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kifuan/qq-chat-history',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
