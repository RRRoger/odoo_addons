# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import logging
import json
import datetime
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class ImportQueryStatementWizard(models.TransientModel):
    _name = 'import.query.statement.wizard'

    file_name = fields.Char('文件名')
    file = fields.Binary('文件')

    def confirm_button(self):
        try:
            _ids = []
            main_obj = self.env["hs.query.statement"].with_context(active_test=False)
            data = json.loads(base64.b64decode(self.file))
            for row in data:
                name = row['name']
                search_ids = main_obj.search([('name', '=', name)])
                if search_ids:
                    name = "{}(copy)".format(name)

                code = row['code']
                search_ids = main_obj.search([('code', '=', code)])
                if search_ids:
                    code = "{}(copy)".format(code)

                create_id = main_obj.create({
                    'name': name,
                    'code': code,
                    'sequence': row['sequence'],
                    'note': row['note'],
                    'wizard_name': row['wizard_name'],
                    'statement': row['statement'],
                    'type': row['type'],
                    'output_ids': row['output_ids'],
                }).id
                _ids.append(create_id)

            res = {
                'type': 'ir.actions.act_window',
                'res_model': 'hs.query.statement',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', _ids)],
            }
            return res

        except Exception as e:
            _logger.error(e)
            raise UserError("配置文件不合法!")
        return True
