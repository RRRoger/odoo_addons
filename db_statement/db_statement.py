# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError
import logging
import base64
import requests
import urllib
import excel_adapter

_logger = logging.getLogger(__name__)

DELIMITER = ','


def list2csv(_list):
    """
    list转成csv文本
    :param _list:
    :return:
    """
    if _list and isinstance(_list, list):
        pass
    else:
        return False
    csv_text = u''
    csv_text += u'%s%s\n' % (DELIMITER.join(_list[0].keys()), DELIMITER)
    for r in _list:
        line = u''
        for i in r.values():
            line += u'"%s"%s' % (i or '', DELIMITER)
        csv_text += u'%s\n' % line.replace('\n', '\\n')
    return csv_text


def list2excel(_list):
    """
        list转成csv文本
        :param _list:
        :return:
        """
    if _list and isinstance(_list, list):
        pass
    else:
        return False
    headers = [{'alias': r, 'name': r, 'group': False} for r in _list[0].keys()]
    excel_data = excel_adapter.format_data(headers, _list)
    sheet1_name = u'查询结果'
    base_data = excel_adapter.excel_data_getter_for_xls(sheet1_name, excel_data)
    return base_data


class DbStatement(models.Model):
    
    _name = 'db.statement'
    _order = 'id desc'

    name = fields.Char(u'名称')
    csv_name = fields.Char(u'名称', compute="_get_csv_name")
    sql = fields.Text(u'可执行语句')
    result = fields.Text(u'本次执行结果', copy=False)
    csv = fields.Binary(u'csv', compute="_get_csv_file")
    brief_result = fields.Text(u'执行结果', compute="_get_brief_result", readonly=1)
    active = fields.Boolean(u'有效', default=True)

    excel_file_name = fields.Char('Excel Name', compute="_get_excel_file_name")
    excel_file = fields.Binary('Excel', attachment=True, compute="_get_excel_file")

    @api.depends('name')
    def _get_csv_name(self):
        for record in self:
            if record.name:
                record.csv_name = u'%s.csv' % record.name
            else:
                record.csv_name = False

    @api.depends('name')
    def _get_excel_file_name(self):
        for record in self:
            if record.name:
                record.excel_file_name = u'%s.xlsx' % record.name
            else:
                record.excel_file_name = False

    @api.depends('result')
    def _get_brief_result(self):
        for record in self:
            if record.result:
                if len(record.result) > 100:
                    record.brief_result = u"%s......" % record.result[:100]
                else:
                    record.brief_result = record.result
            else:
                record.brief_result = False

    @api.depends('result')
    def _get_csv_file(self):
        for record in self:
            if record.result:
                try:
                    result = eval(record.result)
                except Exception:
                    result = False
                    _logger.warning(u'[db.statement] result 不可 eval')
                if result:
                    csv_text = list2csv(result)
                    # record.csv = base64.encodestring(csv_text)
                    record.csv = base64.b64encode(csv_text.encode(encoding='utf-8'))
                else:
                    record.csv = False
            else:
                record.csv = False

    @api.depends('result')
    def _get_excel_file(self):
        for record in self:
            if record.result:
                try:
                    result = eval(record.result)
                except Exception:
                    result = False
                    _logger.warning(u'[db.statement] result 不可 eval')
                record.excel_file = False
                if result:
                    excel_data = list2excel(result)
                    record.excel_file = base64.b64encode(excel_data)
                else:
                    record.excel_file = False
            else:
                record.excel_file = False

    @api.multi
    def button_execute_sql(self):
        cr = self.env.cr
        if self._uid != SUPERUSER_ID:
            raise UserError(u"只有Administrator可操作.")
        for obj in self:
            sql = obj.sql.strip()
            if not sql:
                raise UserError(u"没有可执行sql语句.")
            try:
                cr.execute(sql)
                if sql[:6].lower() == 'select':
                    res = cr.dictfetchall()
                else:
                    res = 'success'
                cr.commit()
            except Exception, e:
                res = str(e)
                cr.rollback()
            obj.write({
                'result': str(res),
            })
        return True

    def get_emails(self, email):
        email_list = email.split('\n')
        real_email_list = []
        for el in email_list:
            if el.startswith('//') or not el:
                pass
            else:
                real_email_list.append(el)
        if not real_email_list:
            raise UserError(u"请正确配置邮箱!")
        return ';'.join(real_email_list)

    @api.one
    def btn_send_mail(self, emails=None):
        if self._uid != SUPERUSER_ID:
            raise UserError(u"只有Administrator可操作.")

        env = self.env
        if not emails:
            raise UserError(u"请先配置接收邮箱用`换行符`隔开!")

        email_api_user = env["ir.config_parameter"].sudo().get_param("email_api_user", default="hesaierp")
        email_api_key = env["ir.config_parameter"].sudo().get_param("email_api_key", default="G6EJfMCrj16njjI9")
        email_api_sender = env["ir.config_parameter"].sudo().get_param("email_api_sender", default="ERP@hesaitech.net")
        email_api_sender_name = env["ir.config_parameter"].sudo().get_param("email_api_sender_name", default="ERP")
        url = "http://api.sendcloud.net/apiv2/mail/send"
        desp = 'application/octet-stream'

        params = {
            "apiUser": email_api_user,
            "apiKey": email_api_key,
            "from": email_api_sender,
            "fromName": email_api_sender_name,
            "to": self.get_emails(emails),
            "subject": u'语句操作结果-%s' % self.name,
            "html": u'<div>语句操作执行结果见附件</div>'
        }

        attachments = [
            ("attachments", (urllib.quote(self.excel_file_name.encode('utf8')), base64.b64decode(self.excel_file), desp)),
        ]

        try:
            r = requests.post(url=url, data=params, files=attachments)
            res = r.json()
            if res['result']:
                pass
            else:
                raise UserError(res['message'])

            env['ir.config_parameter'].sudo().set_param('db_stat.mail_to', emails)

        except Exception, e:
            env.cr.rollback()
            raise UserError("Unknown error: %s" % str(e).decode('unicode-escape'))

        return True

    @api.multi
    def unlink(self):
        raise UserError(u"就不让你删!\n不让你删!\n让你删!\n你删!\n删!\n!\n")
