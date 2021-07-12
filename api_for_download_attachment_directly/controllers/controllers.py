# -*- coding: utf-8 -*-
from odoo import http, tools
from odoo.http import request, content_disposition
from ..models.attachment_factory import AttachmentFactoryErr
import base64


class ApiForDownloadAttachment(http.Controller):

    @http.route('/web/download/attachment/<string:code>', type='http', auth="none", csrf=False)
    def get_lidar_type_marking_template(self, code, *args, **data):
        main_obj = request.env['attachment.factory'].sudo()
        af = main_obj.search([("name", "=", code)], limit=1)
        if not af:
            raise AttachmentFactoryErr("File data not found.")
        try:
            model = af.model
            res_id = af.res_id
            model_field = af.model_field
            filename_field = af.filename_field

            this = request.env[model].sudo().browse(res_id)
            file_data = getattr(this, model_field)
            filename = getattr(this, filename_field)

            return request.make_response(base64.b64decode(file_data),
                                         [('Content-Type', 'application/octet-stream'),
                                          ('Content-Disposition',
                                           content_disposition(filename))])
        except Exception as e:
            raise AttachmentFactoryErr(tools.ustr(e))
