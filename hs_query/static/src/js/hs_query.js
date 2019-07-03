odoo.define('hs_query', function (require) {
    "use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');
    var ajax = require('web.ajax');
    var translation = require('web.translation');
    var ActionManager = require('web.ActionManager');
    var _t = translation._t;

    /* Roger's code blow */

    // jump to show data page
    var query_page = Widget.extend({
        start: function () {
            var self = this;
            var context = {};
            var parent = self.getParent()

            //console.log(self);

            // >_< ....
            // context 在 parent.action_stack 的最后一个元素 的 action_descr
            context = parent.action_stack.slice(-1)[0].action_descr.context

            ajax.jsonRpc('/query/page/', 'call', {
                context: context,
            }).then(function (result) {
                self.$el.append(result)
            });
        }
    });

    core.action_registry.add('hs_query.sys_query_report', query_page);

    // Homepage
    var homepage = Widget.extend({
        start: function () {
            var self = this;
            ajax.jsonRpc('/query/homepage/', 'call', {
            }).then(function (result) {
                self.$el.append(result)
            });
        }
    });

    core.action_registry.add('hs_query.sys_query_homepage', homepage);

    /* Roger's code end */
});
