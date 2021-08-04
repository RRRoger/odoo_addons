odoo.define('hs_query', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var ajax = require('web.ajax');

    /* Roger's code blow */

    function get_ctx(_parent){
        /* 获取最新的action的context */
        let res = {};
        let tmp = 0;
        let prefix = 'action_'
        for(let ac_name in _parent.actions){
            let ac_index = ac_name.split('_')[1] * 1;
            if(ac_index > tmp){
                tmp = ac_index
            }
        }
        return _parent.actions[prefix + tmp].context
    };

    // jump to show data page
    var QueryPage = AbstractAction.extend({
        start: function () {
            var self = this;
            var context = {};
            var parent = self.getParent()

            //console.log(self);

            // >_< ....
            // context 在 parent.action_stack 的最后一个元素 的 action_descr
            let this_ctx = get_ctx(parent);

            ajax.jsonRpc('/query/page/', 'call', {
                context: this_ctx,
            }).then(function (result) {
                self.$el.append(result)
            });
        }
    });

    core.action_registry.add('hs_query.sys_query_report', QueryPage);

    // Homepage
    var Homepage = AbstractAction.extend({
        start: function () {
            var self = this;
            ajax.jsonRpc('/query/homepage/', 'call', {
            }).then(function (result) {
                self.$el.append(result)
            });
        }
    });

    core.action_registry.add('hs_query.sys_query_homepage', Homepage);

    return {
        Homepage: Homepage,
        QueryPage: QueryPage
    };

    /* Roger's code end */
});
