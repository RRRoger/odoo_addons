# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.base.ir.ir_actions import IrActionsServer
import json
# import base64

CODE_DESC_HEAD = """# Add IN module ir_actions_enhance
#  - json_dumps from json: Python libraries
# ******
"""


class IrActionsServerExtends(models.Model):
    _inherit = 'ir.actions.server'

    DEFAULT_PYTHON_CODE = CODE_DESC_HEAD + IrActionsServer.DEFAULT_PYTHON_CODE

    code = fields.Text(default=DEFAULT_PYTHON_CODE)

    @api.model
    def _get_eval_context(self, action=None):
        """
            add json.dumps
            add base64.b64encode
            add base64.b64decode
        :param action:
        :return:
        """
        res_data = super(IrActionsServerExtends, self)._get_eval_context(action=action)
        res_data['json_dumps'] = json.dumps
        # res_data['base64_b64encode'] = base64.b64encode
        # res_data['base64_b64decode'] = base64.b64decode
        return res_data
