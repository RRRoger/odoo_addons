//对string对象新增函数 格式化字符串 仿照python风格
String.prototype.format= function(){
   var args = arguments;
   return this.replace(/\{(\d+)\}/g,function(s,i){
     return args[i];
   });
};

function alert_msg(...args) {
    console.log(args);
    args[0] = "<br/><br/><h3 style='text-align:center;'>{0}</h3><br/><br/>".format(args[0]);
    bootbox.alert(...args);
    return
};

// datatables 中文翻译
var language = {
    //这里很重要，如果你的加载中是文字，则直接写上文字即可，如果是gif的图片，使用img标签就可以加载,
    "sProcessing":   "<img src='/hs_query/static/description/loading-icon.gif'>",

    "sLengthMenu":   "显示结果数目 _MENU_",
    "sZeroRecords":  "没有匹配结果",
    "sInfo":         "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
    "sInfoEmpty":    "显示第 0 至 0 项结果，共 0 项",
    "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
    "sInfoPostFix":  "",
    "sSearch":       "搜索:",
    "sUrl":          "",
    "sEmptyTable":     "表中数据为空",
    "sLoadingRecords": "载入中...",
    "sInfoThousands":  ",",
    "oPaginate": {
        "sFirst":    "首页",
        "sPrevious": "上页",
        "sNext":     "下页",
        "sLast":     "末页"
    },
    "oAria": {
        "sSortAscending":  ": 以升序排列此列",
        "sSortDescending": ": 以降序排列此列"
    }
};

var columnDefs = [
    {
        "searchable": false,
        "orderable": false,
        "targets": 0  //  这个参数是一个列定义对象数组，通过使用 columnDefs.targetsDT 选项，
                      //  告诉Datatables是定义的是那一列，他可以是下列情况：
                      //     0或者正整数-列从左到右是从0开始
                      //      一个负数-列从右到左的索引(-1代表最后一列)
                      //      一个字符串-将字符串和类名匹配列
                      //      字符串"_all"-所有列
    }];

var order = [[ 1, 'asc' ]];