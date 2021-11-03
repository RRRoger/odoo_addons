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

    statement_code = fields.Char(u"code")

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
