# -*- coding: utf-8 -*-
import logging
import sys

import os
import json
import jinja2
from odoo.http import request
from odoo import http
from odoo.addons.hs_query.libs.query_libs import get_query_statement_by_code
_logger = logging.getLogger(__name__)


FORMAT_TIME = '%Y-%m-%d %H:%M:%S'


if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'html'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('odoo.addons.hs_query', "html")

jinja_env = jinja2.Environment('<%', '%>', '${', '}', '%', loader=loader, autoescape=True)

reload(sys)
sys.setdefaultencoding('utf-8')


class QueryController(http.Controller):

    # show-page 模块菜单主页
    @http.route('/query/homepage/', type='json', auth='user', csrf=False)
    def query_homepage(self, *args, **kwargs):
        template = jinja_env.get_template("query_index.html")
        data = {}
        render_val = template.render(data)
        return render_val

    # show-page 展示数据
    @http.route('/query/page/', type='json', auth='user', csrf=False)
    def query_page(self, *args, **kwargs):
        template = jinja_env.get_template("data_query.html")

        ctx = request._context

        _statement_code = ctx.get('_statement_code', '')
        query = get_query_statement_by_code(request.env, _statement_code)

        if not query:
            return "<div style='font-size:16px'>暂无数据</div>"

        columns = query.get_columns()

        data = {
            'columns': json.dumps(columns, ensure_ascii=False),
            'context': json.dumps(ctx, ensure_ascii=False),
        }
        render_val = template.render(data)
        return render_val

    # query-data 展示数据
    @http.route('/query/data', type='json', auth='user', csrf=False)
    def query_data(self, *args, **kwargs):
        return request.env['hs.query.adapter'].query_data(*args, **kwargs)

