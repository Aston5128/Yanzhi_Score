# 利用微软小冰 API 接口，对大量照片进行颜值评分

	环境
	python3 with requests、SQLAlchemy
	任意 SQL 数据库

## 项目动机
朋友有 3000+ 张照片需要用微软小冰来评比颜值，但是小冰 API 有访问限制（每分钟10次，每小时60次，每天360次），如果单纯使用一台机子，需要八天。然而这并难不倒我，利用学校的机房来集群获取评分，这样的话，开10台机器，在一个小时的效率比一台机器一天的效率都要高。

主机运行 Commander，从机运行 Soldier。
Commander      主要用来分配任务、发送资源（照片）以及接收与处理士兵返回的报告
Soldier        接收 Commander 发出的命令和资源，去请求微软小冰的 API

数据库使用 SQLAlchemy 框架，屏蔽底层数据库差异
Soldier 依赖于 requests

## 使用方法
控制机运行 Commander

	python3 Commander/database.py          # 创建表，自行填充数据，database.py 可以根据自己来定制
	python3 Commander                      # 开启 Commander
从机运行   Soldier

	python3 Soldier                        # 开启 Soldier

### 版本

#### Version 0.0.1（2019/3/20）
针对微软小冰 API 访问限制，利用机房资源集群获取照片评分。
控制机（Commander）和士兵机（Soldier）
初代版本还有一些 BUG 未解决
