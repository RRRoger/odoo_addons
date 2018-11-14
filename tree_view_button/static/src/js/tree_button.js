odoo.define('roger.tree_buttons_action', function (require) {
    "use strict";

    var ListView = require('web.ListView');
    var data = require('web.data');
    var Model = require('web.DataModel');
    var web_client = require('web.web_client');
    var session = require('web.session');

    // 判断obj是不是字段
    function isJson(obj){
        return typeof(obj) == "object" && Object.prototype.toString.call(obj).toLowerCase() == "[object object]" && !obj.length;
    };

    function tree_buttons_action (bt) {

        //bt[0] 是方法名
        //bt[1] 是button展示字符串

        var self = this;
        var model_name = this.model;
        console.log(model_name);
        var res= false;
        new Model(model_name).call(bt[0], [this.model], {
            context: this.dataset.context,
            select_ids: self.groups.get_selection().ids,
        }).done( function (data) {
            //console.log(data);

            //处理后台返回的data
            if(isJson(data)){
                web_client.action_manager.do_action(data);
            }
        });
        return res;
    };

    function setOptionsButtons(self, buttons){
        session.rpc('/web/dataset/call_kw', {
            model: 'tvb.adapter',
            method: 'button_filter',
            args: [1, JSON.stringify(buttons)],
            kwargs: {context: self.dataset.context}
        }).then(function (results) {
            if (results.length>0) {
                self.options.buttons = results;
            } else {
                self.options.buttons = [];
            }
        }, null);
    };

    ListView.include({
        init: function() {
            this._super.apply(this, arguments);
            if(this.is_action_enabled('buttons')){
                setOptionsButtons(this, this.is_action_enabled('buttons'))
            }
        },
        render_buttons: function() {
            var self = this;
            var add_button = false;
            if (!this.$buttons) {
                add_button = true;
            }
            this._super.apply(this, arguments);
            let buttons = this.options.buttons;
            console.log(buttons);
            if(add_button && buttons){
                for(var i=0; i<buttons.length; i++){
                    this.$buttons.on('click', '.o_tree_bt_' + buttons[i][0], tree_buttons_action.bind(this, buttons[i]));
                }
            }
        }
    });
});
