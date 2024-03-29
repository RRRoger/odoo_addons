# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.http import request
from uuid import uuid4
import logging
import datetime
_logger = logging.getLogger(__name__)


class AttachmentFactoryErr(Exception):
    """
        Attachment Factory Exception
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class AttachmentFactory(models.Model):
    _name = 'attachment.factory'

    name = fields.Char("Name", readonly=True, index=True)
    model = fields.Char("Model")
    res_id = fields.Integer('ID', index=True)
    model_field = fields.Char("Model Field")
    filename_field = fields.Char("Field Name")
    is_temporary = fields.Boolean("Is Temporary", default=True)
    note = fields.Char("Note")

    @api.model
    def create(self, values):
        values['name'] = str(uuid4())
        create_inst = super(AttachmentFactory, self).create(values)
        return create_inst

    @property
    @api.multi
    def filename(self):
        try:
            this = self.env[self.model].browse(self.res_id)
            fname = getattr(this, self.filename_field)
            return fname
        except Exception as e:
            raise AttachmentFactoryErr("Filename not found.")

    @property
    @api.multi
    def url(self):

        try:
            url_root = request.httprequest.url_root
        except Exception, e:
            url_root = self.sudo().env['ir.config_parameter'].get_param('web.base.url') + '/'

        return "{base_url}web/download/attachment/{name}".format(**{
            "base_url": url_root,
            "name": self.name,
        })

    def delete_expired_file(self, days=7):
        _logger.info("[Api For Download Attachment Directly] Start to delete expired files, days={} ~~".format(days))
        now = datetime.datetime.now() + datetime.timedelta(days=-days)
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        sql = """ delete from attachment_factory where create_date < '{}' and is_temporary; """.format(now)
        self._cr.execute(sql)
        return True
