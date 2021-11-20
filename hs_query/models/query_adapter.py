# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.http import request, content_disposition
from odoo.addons.hs_query.libs.query_libs import query_and_count_data, get_query_statement_by_code
import json
import traceback

ERROR_NO_STATEMENT_CODE = u"数据库查询代码[ %s ]不存在, 请联系管理员!!"
ERROR_SQL_QUERY = u"数据库查询异常, 请联系管理员!!<br/><br/> %s"


class QueryAdapter(models.TransientModel):

    _name = 'hs.query.adapter'

    def query_data(self, *args, **kwargs):

        # 接口传值
        query_condition = request.jsonrequest['context'].get('query_condition', {}) or {}
        _statement_code = request.jsonrequest['context']['_statement_code']

        query = get_query_statement_by_code(request.env, _statement_code)

        if not query:
            return {
                'error': 1,
                'msg': ERROR_NO_STATEMENT_CODE % _statement_code,
            }

        sql = query.statement or ''
        wizard_name = query.wizard_name or ''

        page = request.jsonrequest['page']  # 页码
        page_size = request.jsonrequest['pagesize']  # 每页显示数量

        # try_catch
        try:
            sql = request.env[wizard_name].format_sql_by_condition(sql, query_condition)
            data = query_and_count_data(self.env, sql, page, page_size, query.get_columns())
        except Exception, e:
            print(traceback.format_exc())
            data = {'error': 1, 'msg': ERROR_SQL_QUERY % str(e)}
        return data

    def query_download(self, statement_code):
        wizard = self.env['query.select.wizard.parent']
        download_data = wizard._generate_download_data(statement_code=statement_code)
        xls_name = download_data['xls_name']
        base_data = download_data['base_data']
        query_id = download_data['query_id']
        wizard.create_download_file(xls_name, base_data, query_id)
        return request.make_response(
            base_data,
            headers=[
                ('Content-Disposition', content_disposition(xls_name)),
                ('Content-Type', 'application/octet-stream')],
        )
