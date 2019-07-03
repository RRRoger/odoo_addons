# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.http import request
from odoo.addons.hs_query.libs.query_libs import query_and_count_data, get_query_statement_by_code
import json

ERROR_NO_STATEMENT_CODE = u"数据库查询代码[ %s ]不存在, 请联系管理员!!"
ERROR_SQL_QUERY = u"数据库查询异常, 请联系管理员!!<br/><br/> %s"


class QueryAdapter(models.TransientModel):

    _name = 'hs.query.adapter'

    def query_data(self, *args, **kwargs):

        # 接口传值
        query_condition = request.jsonrequest['context']
        _statement_code = query_condition['_statement_code']

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
            data = {'error': 1, 'msg': ERROR_SQL_QUERY % str(e)}

        return data
