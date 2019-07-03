# -*- coding: utf-8 -*-


def format_cols(columns):
    sel_fields = []
    for col in columns:
        if col['alias'] == '__index__':
            sel_fields.append("row_number() OVER () AS %s" % col['alias'])
        else:
            sel_fields.append('__ft__."%s" AS "%s"' % (col['alias'], col['alias']))
    sel_sql_header = ',\n'.join(sel_fields)
    return sel_sql_header


def format_paging_sql(sql, page, page_size, columns):
    """
        分页格式化sql
    :param sql:
    :param page:
    :param page_size:
    :param columns:
    :return:
    """

    sel_sql_header = format_cols(columns)

    if not any([page, page_size]):
        limit_offset_sql = ''
    else:
        limit_offset_sql = ' LIMIT %(limit)s OFFSET %(offset)s ' % dict(limit=page_size, offset=page_size * (page - 1))

    sql = """
SELECT
    %(sel_sql_header)s
FROM
    ( %(sql)s ) __ft__ 
%(limit_offset_sql)s
    """ % dict(sql=sql, sel_sql_header=sel_sql_header, limit_offset_sql=limit_offset_sql)

    return sql


def format_count_sql(sql):
    """
        格式化总记录sql
    :param sql:
    :return:
    """
    sql = """

    SELECT count(1) FROM (
        %(sql)s
    ) __ft__
    """ % dict(sql=sql)
    return sql


def query_data(env, sql, page, page_size, columns, return_dict=False):
    """
        分页查询
    :param env:
    :param sql:
    :param page:
    :param page_size:
    :param columns:
    :param return_dict:
    :return:
    """
    cr = env.cr
    _sql = format_paging_sql(sql, page, page_size, columns)
    cr.execute(_sql)
    if return_dict:
        return cr.dictfetchall()
    else:
        return cr.fetchall()


def count_data(env, sql):
    """
        查询总记录条数
    :param env:
    :param sql:
    :return:
    """
    cr = env.cr
    _sql = format_count_sql(sql)
    cr.execute(_sql)
    return cr.fetchone()[0]


def query_and_count_data(env, sql, page, page_size, columns):
    """
        分页查询 & 查询总记录条数
    :param env:
    :param sql:
    :param page:
    :param page_size:
    :param columns:
    :return:
    """
    return {
        'data_set': query_data(env, sql, page, page_size, columns),
        'total_count': count_data(env, sql),
    }


def get_query_statement_by_code(env, _statement_code):
    return env['hs.query.statement'].search([('code', '=', _statement_code)], limit=1)
