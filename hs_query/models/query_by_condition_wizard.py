# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import logging
import json
import datetime
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class QueryByConditionWizard(models.TransientModel):
    _name = 'query.by.condition.wizard'

    user_id = fields.Many2one('res.users', u'用户')
    user_ids = fields.Many2many('res.users', string=u'用户(多选)')
    start_date = fields.Date(u"开始日期")
    end_date = fields.Date(u"结束日期")
    start_time = fields.Datetime(u"开始时间")
    end_time = fields.Datetime(u"结束时间")
    content = fields.Char(u"匹配文本")

    statement_name = fields.Char(u"name")
    statement_code = fields.Char(u"code")
    statement_note = fields.Char(u"说明")

    clear = fields.Boolean(u"清空条件")

    @api.onchange('clear')
    def onchange_clear(self):
        if self.clear:
            self.user_ids = [(6, 0, [])]
            self.user_id = False
            self.start_date = False
            self.end_date = False
            self.start_time = False
            self.end_time = False
            self.content = False

    @api.onchange('statement_code')
    def onchange_statement_code(self):
        parent_obj = self.env['query.select.wizard.parent']
        condition_and_desc = parent_obj.get_query_condition_and_desc(self.statement_code)
        condition = condition_and_desc.get('query_condition', {})
        if condition:
            self.user_ids = [(6, 0, condition.get('USER_IDS') or [])]
            self.user_id = condition.get('UID') or False
            self.start_date = condition.get('START_DATE') or ''
            self.end_date = condition.get('END_DATE') or ''
            self.start_time = condition.get('START_TIME') or ''
            self.end_time = condition.get('END_TIME') or ''
            self.content = condition.get('CONTENT') or ''

    @api.multi
    def create_cache(self):
        self.ensure_one()
        condition_desc = ""
        if self.user_id:
            condition_desc += "用户: {}<br/>".format(self.user_id.name)
        if self.user_ids:
            condition_desc += "用户: {}<br/>".format(';'.join(u.name for u in self.user_ids))
        if self.start_date:
            condition_desc += "开始日期: {}<br/>".format(self.start_date)
        if self.end_date:
            condition_desc += "结束日期: {}<br/>".format(self.end_date)
        if self.start_time:
            condition_desc += "开始时间: {}<br/>".format(self.start_time)
        if self.end_time:
            condition_desc += "结束时间: {}<br/>".format(self.end_time)
        if self.content:
            condition_desc += "匹配文本: {}<br/>".format(self.content)

        query_condition = {
            'UID': self.user_id.id or 0,
            'USER_IDS': self.user_ids.ids or [],
            'START_DATE': self.start_date or '',
            'END_DATE': self.end_date or '',
            'START_TIME': self.start_time or '',
            'END_TIME': self.end_time or '',
            'CONTENT': self.content or '',
        }

        self.env['query.select.wizard.parent'].create_cache(self.statement_code, query_condition, condition_desc)

    @api.multi
    def confirm_button(self):
        self.ensure_one()
        self.create_cache()
        wizard_parent = self.env['query.select.wizard.parent']
        return wizard_parent._confirm(self.statement_code)

    @api.multi
    def download_data(self):
        self.ensure_one()
        self.create_cache()
        wizard_parent = self.env['query.select.wizard.parent']
        return wizard_parent._download(self.statement_code)
