# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class DbStatSendMailWizard(models.TransientModel):
    _name = "db.stat.send.mail.wizard"
    _description = "Db Stat Send Mail Wizard"

    emails = fields.Text(string=u"收件人")

    @api.model
    def default_get(self, fields_list):
        res = dict()
        res['emails'] = self.env['ir.config_parameter'].sudo().get_param('db_stat.mail_to') or ''
        return res

    @api.multi
    def confirm_button(self):
        self.ensure_one()
        context = dict(self._context or {})
        obj_id = context.get('active_id', False)
        obj = self.env['db.statement'].browse(obj_id)
        emails = self.emails
        obj.btn_send_mail(emails=emails)
        return {
            "type": "ir.actions.client",
            "tag": "action_notify",
            "params": {
                "title": 'Ok',
                "text": 'OK!!!',
                "sticky": False
            }
        }













