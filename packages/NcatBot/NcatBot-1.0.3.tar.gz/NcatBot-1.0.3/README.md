# NcatBot SDK

NcatBot SDK 是一个用于创建和管理QQ机器人的Python库。它提供了丰富的API来发送消息、处理事件和执行其他机器人相关的任务。

## 安装

要安装QQBot SDK，你可以使用pip：

```bash
pip install NcatBot
```

## 快速开始

以下是如何使用QQBot SDK来创建一个简单的机器人：

```python
from qqbot import GroupHttper, PrivateHttper, OtherHttper

# 初始化机器人
group_httper = GroupHttper("http://your-api-url")
private_httper = PrivateHttper("http://your-api-url")
other_httper = OtherHttper("http://your-api-url")

# 发送群消息
group_httper.send_group_msg(group_id=12345, text="Hello, QQ Group!")

# 发送私聊消息
private_httper.send_private_msg(user_id=67890, text="Hello, QQ User!")

# 获取登录信息
login_info = other_httper.get_login_info()
print(login_info)
```


## 贡献

我们欢迎任何形式的贡献，包括代码、文档、bug报告和功能请求。如果你想要参与开发，请查看我们的 贡献指南 。

## 许可证

QQBot SDK 是在 MIT 许可证下发布的。详情请参阅 LICENSE 文件。

