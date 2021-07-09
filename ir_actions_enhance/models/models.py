# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.base.ir.ir_actions import IrActionsServer
import json
import re
import base64
import string

CODE_DESC_HEAD = """# Add Some Frequently-Used libraries In hesai_main By Roger
# - json, re, base64, string: Python libraries
# * * * * * * * * * * *
"""


class IrActionsServerExtends(models.Model):
    _inherit = 'ir.actions.server'

    DEFAULT_PYTHON_CODE = CODE_DESC_HEAD + IrActionsServer.DEFAULT_PYTHON_CODE
    code = fields.Text(default=DEFAULT_PYTHON_CODE)

    @api.model
    def _get_eval_context(self, action=None):
        """ 添加几个常用的python库 """
        res_data = super(IrActionsServerExtends, self)._get_eval_context(action=action)
        res_data['json'] = json
        res_data['re'] = re
        res_data['base64'] = base64
        res_data['string'] = string
        return res_data
