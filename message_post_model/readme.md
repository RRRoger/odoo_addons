# 消息发布日志
> 作者: [http://www.vauxoo.com](http://www.vauxoo.com)

### [英文文档](README_EN.rst)

> 此模块在任何具有对象继承的模型中添加扩展日志 为每个更改创建字段message_ids（mail.message） 该模型的领域不同于Odoo所做的传统方式。

## 特性

我们添加了两个服务器操作来添加o删除模型中的功能 你不需要直接修改代码，至少你的模型没有 与mail.message有直接关系

在ir.model对象中，我们添加了三个新字段：

> ![](https://api.superbed.cn/pic/5c139027c4ff9e2b4e044c61)
> - 跟踪：`Boolean`，用于标记模型是否已激活跟踪
> - 排除字段：`Many2many`，排除一些不需要跟踪的字段
> - 排除外部字段：`Char` 多个字段组合成的字符串, 与对象没有直接关系。这个字段必须是由`,`分隔，中间没有空格。例如 product_uom_qty,product_uos_qty,name

- 添加跟踪：

![](https://api.superbed.cn/pic/5c1391ccc4ff9e2b4e044c63)

- 删除跟踪：

![](https://api.superbed.cn/pic/5c1391b4c4ff9e2b4e044c62)



- 此刻，在每个更改记录中添加对象的跟踪 有消息留在日志中
- 如果要排除模型的某些字段，以避免产生消息 这些字段已更改，您可以使用“排除字段”字段进行说明
- 在某些情况下，您需要排除没有直接的字段 主模型的关系（订单行中的数量）和这些不相关排除字段中的出现（many2many with domain）。对于这些领域存在的 “排除外部字段”，您可以在其中单独指定此字段，用`,`分隔，他们之间没有空格

- 此外，如果您需要它，还有一个名为message_post_test的测试模块 证明功能.
