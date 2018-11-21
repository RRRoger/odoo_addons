# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError
import logging
import base64

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


class DbStatement(models.Model):
    
    _name = 'db.statement'
    _order = 'id desc'

    name = fields.Char(u'名称')
    csv_name = fields.Char(u'名称', compute="_get_csv_name")
    sql = fields.Text(u'可执行语句')
    result = fields.Text(u'本次执行结果')
    csv = fields.Binary(u'csv', compute="_get_csv_file")
    brief_result = fields.Text(u'执行结果', compute="_get_brief_result", readonly=1)

    @api.depends('name')
    def _get_csv_name(self):
        for record in self:
            if record.name:
                record.csv_name = u'%s.csv' % record.name
            else:
                record.csv_name = False

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

