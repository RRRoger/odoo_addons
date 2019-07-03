
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError


class QueryDemoReportWizard(models.TransientModel):

    _name = 'query.demo.report.wizard'

    # 必须继承
    _inherit = 'query.select.wizard.parent'

    # 唯一code
    _statement_code = 'query_demo_report'


