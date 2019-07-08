# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
from odoo.addons.hs_query.libs.query_libs import get_query_statement_by_code, query_data
from odoo.addons.hs_query.libs import excel_adapter
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import logging
import json
import datetime
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

TAG = "hs_query.sys_query_report"


class QuerySelectWizardParent(models.AbstractModel):
    _name = 'query.select.wizard.parent'

    _statement_code = ''

    @api.model
    def default_get(self, fields_list):
        """
            默认数据, 获取上一次查询条件, 更新默认值
        :param fields_list:
        :return:
        """
        defaults = super(QuerySelectWizardParent, self).default_get(fields_list)
        cache_obj = self.env['hs.query.input.cache']
        cache = cache_obj.search([
            ('statement_code', '=', self._statement_code),
            ('user_id', '=', self._uid),
        ], limit=1, order='id desc')
        if cache:
            defaults = json.loads(cache.query_condition)
        return defaults

    def create_cache(self, query_condition, condition_desc='', _uid=None):
        """
            创建查询条件缓存
        :param query_condition:
        :param condition_desc:
        :param _uid:
        :return:
        """
        cache_obj = self.env['hs.query.input.cache']
        if not _uid:
            _uid = self._uid

        _sql = """
DELETE FROM 
    hs_query_input_cache 
WHERE user_id = %s and statement_code = '%s';
        """ % (_uid, self._statement_code)
        self._cr.execute(_sql)  # 清空该用户该报表查询条件缓存

        cache_obj.create({
            'user_id': _uid,
            'query_condition': json.dumps(query_condition),
            'condition_desc': json.dumps(condition_desc),
            'statement_code': self._statement_code,
        })

        return True

    def format_condition_desc_for_excel(self):
        """
            excel展示查询条件
            需要返回一个二维数组
        :return:
        """
        return []

    @api.multi
    def confirm(self):
        """
            开始datatables展示
        :return:
        """
        self.ensure_one()
        return self._confirm()

    @api.multi
    def _confirm(self, statement_code=None):
        statement_code = statement_code if statement_code else self._statement_code

        condition_and_desc = self.get_query_condition_and_desc()
        query_condition = condition_and_desc.get('query_condition', {})
        condition_desc = condition_and_desc.get('condition_desc', '')
        self.validate_condition_for_query(query_condition)

        # 返回结果
        res = {
            'type': 'ir.actions.client',
            'tag': TAG,
            'context': {
                '_uid': self._uid,
                '_statement_code': statement_code,
            },
        }

        self.create_cache(query_condition, condition_desc)
        res['context'].update(query_condition)
        res['context'].update({'condition_desc': condition_desc})

        self.env['hs.query.statement'].create_query_record(statement_code, self._uid)
        return res

    @api.multi
    def download(self):
        """
            下载excel
        :return:
        """
        self.ensure_one()
        return self._download()

    def _download(self, statement_code=None):
        statement_code = statement_code if statement_code else self._statement_code

        query = get_query_statement_by_code(self.env, statement_code)
        if not query:
            raise UserError(u"数据库查询代码[ %s ]不存在, 请联系管理员!!" % statement_code)

        sql = query.statement or ""

        # 获取查询条件
        condition_and_desc = self.get_query_condition_and_desc()
        condition = condition_and_desc.get('query_condition', {})
        condition_desc = condition_and_desc.get('condition_desc', '')
        self.create_cache(condition, condition_desc)
        # 检验查询条件
        self.validate_condition_for_download(condition)
        final_sql = self.format_sql_by_condition(sql, condition)

        # 检验显示列
        columns = query.get_columns()

        # 执行sql
        try:
            res_data = query_data(self.env, final_sql, None, None, columns, return_dict=1)
        except Exception, e:
            raise UserError(u"查询出错: \n\n %s" % str(e))

        # 格式化excel需要的数据
        excel_data = excel_adapter.format_data(columns, res_data)

        now = datetime.datetime.now() + datetime.timedelta(hours=8)

        xls_name = u'%s(%s).xlsx' % (query.name, now.strftime('%Y%m%d%H%M%S'))

        # 生成excel所需要的数据
        base_data = excel_adapter.excel_data_getter(u'查询结果', excel_data, u'查询条件', self.format_condition_desc_for_excel())

        # 调用创建下载
        download_file_id = self.create_download_file(xls_name, base_data, query.id)

        view_id = self.env.ref('hs_query.hs_query_download_file_view_form').id

        context = self._context.copy()
        res = {
            'type': 'ir.actions.act_window',
            'res_model': 'hs.query.download.file',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'target': 'new',
            'res_id': download_file_id,
            'context': context,
        }
        return res

    def create_download_file(self, xls_name, base_data, statement_id):
        """
            创建下载文件
        :param xls_name:
        :param base_data:
        :param statement_id:
        :return:
        """
        file_obj = self.env['hs.query.download.file']
        create_id = file_obj.create({
            'file_name': xls_name,
            'file': base64.b64encode(base_data),
            'statement_id': statement_id,
        }).id
        return create_id

    @api.multi
    def get_query_condition_and_desc(self):
        """
            获取查询条件
        :return:
        """
        return {
            'query_condition': {},
            'condition_desc': ""
        }

    def format_sql_by_condition(self, sql, condition):
        """
            根据查询条件格式化sql
        :param sql:
        :param condition:
        :return:
        """
        return sql

    def _validate_condition(self, condition):
        """
            验证查询条件
        :param condition:
        :return:
        """
        return True

    def validate_condition_for_query(self, condition):
        """
            验证查询条件: for 查询展示
        :param condition:
        :return:
        """
        return self._validate_condition(condition)

    def validate_condition_for_download(self, condition):
        """
            验证查询条件: for 下载
        :param condition:
        :return:
        """
        return self._validate_condition(condition)
