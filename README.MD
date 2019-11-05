### 简介
基于django + celery + rabbitmq + wechat + mattermost搭建的一个简单的reminder项目.主要功能有如下三个.
- 生日提醒
- tickets提醒
- exception提醒

### 生日提醒
1. 关注微信号(后台自动生成用户)
2. 登录django 后台，添加birth day记录
3. celery 轮训添加的记录,找到今天生日的记录，通过微信号和mattermost给予提醒


### tickets提醒
通过监听ticket message的创建, 发现ticket的新的ticket,通过mattermost 给予提醒


### exception 提醒
1.为logger.exception添加补丁，调用exception的时候，往mq队列扔信息
2.reminder 监听消息队列，通过mattermost 给予提醒


### 常见问题

#### 1.为什么不使用skype提醒?

我尝试过了，但是没有结果。相比skype我更喜欢mattermot,因为其支持markdown语法,但是mattermost更美观也是原因之一。

#### 2.请检查连接，无法连接mattermost.如果问题持续，请管理员检查websocket端口

这个正常，国内访问偶尔会提示这个问题。

### more
有任何新的想法或者建议，或者实现方式，欢迎私聊,你知道的，我一直都在。

