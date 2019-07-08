# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
import datetime
import logging

_logger = logging.getLogger(__name__)

TYPE_SELECTION = [
    ('sql', u'普通SQL查询',)
]


class QueryStatement(models.Model):

    _name = "hs.query.statement"
    _order = "sequence, id"

    # alter table hs_query_statement drop constraint hs_query_statement_unique_statement_wizard_name ;
    # 删除约束

    _sql_constraints = [
        ('unique_statement_code', 'unique(code)', u'代码不能重复'),
        ('unique_statement_name', 'unique(name)', u'名称不能重复'),
    ]

    name = fields.Char(string=u'名称')
    code = fields.Char(string=u'代码')
    active = fields.Boolean(string=u'有效', default=True)
    type = fields.Selection(TYPE_SELECTION, string=u'类型', default='sql')
    sequence = fields.Integer(string=u'顺序', default=10)
    note = fields.Text(string=u'说明')

    statement = fields.Text(string=u'语句')
    wizard_name = fields.Char(string=u'向导名称', default='query.select.wizard.parent')

    output_ids = fields.One2many('hs.query.statement.output', 'statement_id', string=u'查询输出', copy=True)
    record_ids = fields.One2many('hs.query.record', 'statement_id', string=u'查询记录', copy=False)
    download_ids = fields.One2many('hs.query.download.file', 'statement_id', string=u'下载记录', copy=False)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default['name'] = self.name + "(copy)"
        default['code'] = self.code + "(copy)"
        default['wizard_name'] = "query.select.wizard.parent"
        return super(QueryStatement, self).copy(default)

    @api.multi
    def get_columns(self):
        self.ensure_one()
        columns = [{"title": u"序号", "alias": "__index__", "name": u"序号", "group": ""}]
        for output in self.output_ids:
            columns.append({
                'title': output.name,
                'name': output.name,
                'alias': output.alias,
                "group": "",
            })
        return columns

    def create_query_record(self, statement_code, user_id):
        """
        创建查询记录
        :param statement_code:
        :param user_id:
        :return:
        """
        query = self.search([('code', '=', statement_code)], limit=1)
        if query:
            query.write({'record_ids': [(0, 0, {'user_id': user_id})]})
        return True

    @api.multi
    def jump2page(self):
        """
            开始datatables展示
        :return:
        """
        self.ensure_one()
        wizard_parent = self.env['query.select.wizard.parent']
        return wizard_parent._confirm(self.code)

    @api.multi
    def download_data(self):
        self.ensure_one()
        wizard_parent = self.env['query.select.wizard.parent']
        return wizard_parent._download(self.code)


class QueryStatementOutput(models.Model):

    _name = "hs.query.statement.output"
    _order = "sequence, id"

    _sql_constraints = [
        ('unique_statement_id_name', 'unique(statement_id, name)', u'名称不能重复'),
    ]

    name = fields.Char(string=u'名称')
    statement_id = fields.Many2one("hs.query.statement", string=u"数据库查询")
    sequence = fields.Integer(string=u'顺序', default=10)
    alias = fields.Char(string=u'别名')
    note = fields.Text(string=u'说明')


class QueryInputCache(models.Model):

    _name = "hs.query.input.cache"
    _order = "id desc"

    statement_code = fields.Char(string=u"数据库查询代码")
    user_id = fields.Many2one('res.users', string=u"用户")
    query_condition = fields.Text(string=u"查询条件")
    condition_desc = fields.Text(string=u"查询条件描述", help=u"用于展示在前端!")


class QueryRecord(models.Model):

    _name = "hs.query.record"
    _order = "id desc"

    statement_id = fields.Many2one("hs.query.statement", string=u"数据库查询")
    user_id = fields.Many2one('res.users', string=u"用户")


class QueryDownloadFile(models.Model):

    _name = "hs.query.download.file"
    _order = "id desc"

    statement_id = fields.Many2one("hs.query.statement", string=u"数据库查询")
    user_id = fields.Many2one('res.users', string=u"用户")
    file = fields.Binary(string=u"下载文件", attachment=True)
    file_name = fields.Char(u'文件名')

    def delete_expired_file(self, days=7):
        _logger.info("[Query] Start to delete expired files ~~")
        now = datetime.datetime.now() + datetime.timedelta(days=-days)
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        self.search([('create_date', '<', now)]).unlink()
        return True
