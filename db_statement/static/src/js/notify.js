odoo.define('db_statement', function(require){
    "use strict";
    var ajax        = require('web.ajax');
    var core        = require('web.core');
    var form_common = require('web.form_common');
    var formats     = require('web.formats');
    var Model       = require('web.Model');

    var QWeb        = core.qweb;
    var _t          = core._t;

    var action_notify = function(element, action){
        var params = action.params;
        if(params){
            element.do_notify(params.title, params.text, params.sticky);
        }
        return {'type':'ir.actions.act_window_close'};
    };

    core.action_registry.add('action_notify', action_notify);
});
