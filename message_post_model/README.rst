消息发布日志
================

此模块在任何具有对象继承的模型中添加扩展日志
为每个更改创建字段message_ids（mail.message）
该模型的领域不同于Odoo所做的传统方式。

特征
--------

我们添加了两个服务器操作来添加o删除模型中的功能
你不需要直接修改代码，至少你的模型没有
与mail.message有直接关系

在ir.model对象中，我们添加了三个新字段：

    .. image :: https://drive.google.com/uc?export=view&id=0B2kzKLGF6ZvLRFYwcTBYT2ZUQ1E

    - 已跟踪：一个布尔值，用于指示模型是否已激活轨道
    - 排除字段：一个many2many字段，用于指示是否要排除
      轨道一些与模型相关的领域
    - 排除外部字段：用于指定字段（数据库名称）的字符串
      与对象没有直接关系。这个字段必须是
      由（，）分隔，其中没有空格。例如
      product_uom_qty，product_uos_qty，名称



- 添加跟踪：

    .. image :: https://drive.google.com/uc?export=view&id=0B2kzKLGF6ZvLSWhKOTZFVzRack0

- 删除跟踪：
    .. image :: https://drive.google.com/uc?export=view&id=0B2kzKLGF6ZvLZ1k5dEpBQUpDVUk

此刻，在每个更改记录中添加对象的跟踪
有消息留在日志中

.. image :: https://drive.google.com/uc?export=view&id=0B2kzKLGF6ZvLdkY3aUpNWWJLYjA

如果要排除模型的某些字段，以避免产生消息
这些字段已更改，您可以使用“排除字段”字段进行说明

.. image :: https://drive.google.com/uc?export=view&id=0B2kzKLGF6ZvLaUtPUnMxNE9LMDA

在某些情况下，您需要排除没有直接的字段
主模型的关系（订单行中的数量）和这些不相关
排除字段中的apper（many2many with domain）。对于这些领域存在的
“排除外部字段”，您可以在其中单独指定此字段（，）
他们之间没有空格

.. image :: https://drive.google.com/uc?export=view&id=0B2kzKLGF6ZvLbUxtQlBhdTItekU


此外，如果您需要它，还有一个名为message_post_test的测试模块
证明功能。

要求：
-------------
- 转到https://github.com/Vauxoo/addons-vauxoo并下载repo以安装message_post_model和message_post_test模块。

贡献者
------------

*JoséMorales<jose@vauxoo.com>

维护者
----------

.. image :: https://www.vauxoo.com/logo.png
   ：alt：Vauxoo
   ：target：https：//vauxoo.com

该模块由Vauxoo维护。

一家拉丁美洲公司，提供培训，指导，
开发和实施企业管理
系统并将其整个运营策略基于使用
开源软件及其主要产品是odoo。

要参与此模块，请访问http://www.vauxoo.com。
