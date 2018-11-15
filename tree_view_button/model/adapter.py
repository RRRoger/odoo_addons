# -*- coding: utf-8 -*-
from odoo import models, _
import json
import logging
_logger = logging.getLogger(__name__)


class TvbAdapter(models.AbstractModel):
    """
        关于`tree_view_button`模块的方法写在这里
    """
    _name = 'tvb.adapter'
    _description = 'Tvb Adapter'

    def check_user_groups(self, groups=''):
        """
        :param groups:
            base.group_system,base.group_user
        :return:
        """
        if not groups:
            _logger.info("`groups` has no content.....PASS")
            return True
        res = False
        for group in groups.split(','):
            group = group.strip()
            if self.env.user.has_group(group):
                res = True
                _logger.info("[HAS_GROUP] Check user group [%s] !!!" % group)
                break
            else:
                _logger.info("[HAS_NO_GROUP] Check user group [%s] !!!" % group)
        return res

    def button_filter(self, buttons):
        """
        :param buttons:
            [
                ["btn_do1", "动作1/Action1"],
                ["btn_do2", "动作2/Action2"],
            ]
        :return:
        """
        if not buttons:
            return []
        buttons = json.loads(buttons)
        if not isinstance(buttons, list):
            return []
        delimiter = '/'  # 分隔符
        res = []
        for button in buttons:
            zh, en = button[1].split(delimiter)
            button[1] = zh if self._context.get('lang') == 'zh_CN' else en
            if len(button) > 2 and self.check_user_groups(button[2]):
                res.append(button)
            else:
                res.append(button)
        return res
