# 利用微软小冰 API 接口，对大量照片进行颜值评分

	环境
	python3 with requests、SQLAlchemy
	任意 SQL 数据库

## 项目动机
朋友有 3000+ 张照片需要用微软小冰来评比颜值，但是小冰 API 有访问限制（每分钟10次，每小时60次，每天360次），如果单纯使用一台机子，需要八天

### 版本

#### Version 0.0.1（2019/3/20）
针对微软小冰 API 访问限制，利用机房资源集群获取照片评分。
控制机（Commander）和士兵机（Soldier）
初代版本还有一些 BUG 未解决
