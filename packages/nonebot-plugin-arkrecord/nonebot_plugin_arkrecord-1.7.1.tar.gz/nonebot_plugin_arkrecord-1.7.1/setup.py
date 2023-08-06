# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_arkrecord', 'nonebot_plugin_arkrecord.ark']

package_data = \
{'': ['*'],
 'nonebot_plugin_arkrecord': ['res_file/output_csv/*',
                              'res_file/record_image/*',
                              'resource/*',
                              'resource/images/*',
                              'resource/profile/*',
                              'resource/ttf/*']}

install_requires = \
['BeautifulSoup4',
 'Pillow',
 'XlsxWriter',
 'lxml',
 'matplotlib',
 'nonebot-adapter-onebot>=2.0.0b1,<3.0.0',
 'nonebot2>=2.0.0b4,<3.0.0',
 'requests']

setup_kwargs = {
    'name': 'nonebot-plugin-arkrecord',
    'version': '1.7.1',
    'description': 'Nonebot plugin for fetching and analyzing gacha records of arknights',
    'long_description': '<h1 align="center"><b>nonebot_plugin_arkrecord</b></h1>\n<p align="center">\n    <img src="https://img.shields.io/badge/Python-3.9+-yellow" alt="python">\n    <img src="https://img.shields.io/badge/Nonebot-2.0.0b4-green" alt="python">\n    <img src="https://img.shields.io/badge/Onebot-11-blue" alt="python">\n</p>\n<h2 align="center"><b>欢迎使用明日方舟抽卡分析NoneBot2插件!</b></h2>\n<h4 align="center">本插件为基于python3.9开发的NoneBot2插件，NoneBot2适配器为OneBotV11，当前版本V1.6.2.2\n</h4>\n\n### **若对插件安装、使用有疑问，或在使用中遇到BUG，欢迎在issue区发问；或直接联系作者：QQ 812325695。我将尽可能地排查并解决问题**\n\n\n## **丨插件功能**\n- 调用明日方舟官方抽卡记录api，获取一个月内的抽卡记录，并将记录储存在nonebot的数据库中\n- 在同一个nonebot机器人的数据库中增量储存某玩家的抽卡记录，做到储存、分析长时间段内的抽卡记录\n- 将玩家的抽卡记录制图发送为消息\n\n## **丨插件部署方法**\n\n1、配置SQLite\n\n本插件依赖于SQLite数据库（版本>=3.38）。\n如果在Linux环境下部署机器人，一般无需配置SQLite环境。但如果你的SQLite版本<3.38，建议将版本升级至至少3.38，否则可能导致无法正确生成分析结果。\n\n如果在Windows环境下部署机器人，请参考网络资源（如[菜鸟教程](https://www.runoob.com/sqlite/sqlite-installation.html)）安装SQLite数据库，但无需控制数据库用户、创建数据库表等操作。\n\n2、安装插件\n\n在命令行（cmd）中\n``` shell\npip install nonebot_plugin_arkrecord\n```\n3、配置数据库储存路径\n\n运行本插件前，需要在机器人的 **.env.prod** 文件中配置数据库储存路径，如\n```arkrecord_db_path = "/root/.arkrecord"```\n\n如果你是1.7版本之前就在使用本插件的老用户，可以直接该路径为```arkrecord_db_path = "/root/.arkrecord"```以保证与此前版本保持一致\n\n如果没有配置该路径，插件将无法启动\n\n4、载入插件\n\n载入插件方式与载入其他插件方式相同，即在NoneBot2的`bot.py`中添加一行\n\n```python\nnonebot.load_plugin(\'nonebot_plugin_arkrecord\')\n```\n\n\n\n\n## **丨插件使用方法**\n### **步骤1：token设置**\n\n每个方舟玩家第一次使用该插件时，需要设置token（令牌）。\n**请注意，如果你在不同的nonebot机器人中使用本插件，需要多次设置token，因为不同机器人的数据库是不互通的。**\n\n**1.1 token获取方法**：**在官网登录后**，根据你的明日方舟账号所属的服务器，选择复制以下网址中的内容\n \n官服：https://web-api.hypergryph.com/account/info/hg ，B服：https://web-api.hypergryph.com/account/info/ak-b\n\n\n**1.2 token设置方法**：使用插件命令`方舟抽卡token 页面内容`(自动识别B服、官服token)\n或`方舟寻访token 页面内容`进行设置\n\n如网页中内容为\n```json\n{"status":0,"msg":"OK","data":{"token":"example123456789"}}\n```\n则使用命令 `方舟抽卡token {"status":0,"msg":"OK","data":{"token":"example123456789"}}`。如果使用`方舟抽卡分析`提示无效token，建议重新使用上述方式设置token。\n\n### **步骤2：寻访记录分析**\n\n设置token后，直接使用`方舟抽卡分析`即可，还可以使用`方舟抽卡分析 数字`，分析最近一定抽数的寻访情况\n\n如`方舟抽卡分析 100`分析最近100抽的情况\n\n\n### **插件维护：更新卡池信息与干员头像**\n**全局更新**\n\n使用`方舟卡池更新`命令，自动从PRTS更新卡池信息及干员头像文件\n\n**手动添加卡池**\n\n在卡池开放后，往往需要在数个小时才能从PRTS上获取正确的卡池名称与内容。此时若希望使用本插件，可以使用手动添加卡池功能，命令格式为。需要添加者QQ号是为了防止误添加。\n\n```手动添加卡池|卡池名称|限定类型（限定 非限定）|添加者QQ号```，如\n\n\n```手动添加卡池|万象伶仃|限定|4008208820```\n\n### **导出记录**\n使用`方舟抽卡导出`命令，可以在群聊中导出你当前关联token的储存于插件数据库中的寻访记录。目前只支持在群聊中导出。\n\n### **其他功能**\n使用`方舟抽卡帮助`命令，可以获取插件帮助。 使用`随机干员`命令，随机给出一张干员头像。\n\n## **丨更新日志**\n- v1.6.0 - v1.6.4 更新内容已隐去，详情请查看既往版本的md文件\n- v1.7.0 调整了关键参数配置方式\n- v1.7.0 **调整了token输入方式，现在可以输入整个token网页内容以设置token**\n- v1.7.0 新增了日志系统，现在可以在arkrecord_db_path文件夹下获取运行报错日志\n- v1.7.0 **新增了手动卡池更新命令，再也不用为更新后无法及时获取寻访分析发愁了！（也许）**\n- v1.7.0 优化了数据库读写的逻辑\n\n- v1.7.1 修复了pip缺失BeautifulSoup4依赖的问题\n- v1.7.1 改进了文档中若干处容易被误解的说法\n- v1.7.1 适配了 新增加的卡池类型：中坚寻访\n\n## **| 更新计划**\n- 敬请期待win-exe版方舟抽卡分析小工具\n## **| 参考**\n作图代码参考于\n\n- [nonebot-plugin-gachalogs](https://github.com/monsterxcn/nonebot-plugin-gachalogs)\n\n- [nonebot_plugin_gamedraw](https://github.com/HibiKier/nonebot_plugin_gamedraw)\n\n## **| 开发人员信息**\n主体开发[本人](https://github.com/zheuziihau)\n\n美术资源及需求设计 [@Alnas1](https://github.com/Alnas1)',
    'author': 'kwtk',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/zheuziihau',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
