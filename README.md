整合微信机器人来实现一些的小功能方便日常的一些琐碎流程

[wxbot](https://github.com/youfou/wxpy) 提供所有的微信方面的api。
[schedule](https://github.com/dbader/schedule) 提供对 schedule 方面的支持。
[jieba](https://github.com/fxsjy/jieba) 提供中文分词。
[停用词的词库](https://github.com/dongxiexidian/Chinese/blob/master/stopwords.dat) 
[爬虫支持](https://github.com/SeleniumHQ/selenium) 需要安装 chromedriver。

**Todo**
- ~~每日站报~~
- ~~对禅道的支持~~
- ~~打卡提醒~~
- ~~发周报~~
- ~~每天早上9点30分，36kr新闻爬取~~（还可以更丰富）
- 项目日报集成
- redis 缓存，加速消息反馈
- 数据库迁移脚本，sqlite export & sqlite to mysql & mysql to sqlite （ez）
- 启动脚本 （ez）
- 上下文会话
- 守护进程包活 （这个可以做的非常完善，包括断线后需要登录的邮件推送，不过目前只做守护进程的包活）
- ~~添加分组功能~~ （目前分组太弱了，不过够了目前）
- 个人助手？
- 集成 flask 开发一个方便查看的管理台
