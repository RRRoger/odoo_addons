/*

datatables.js 核心逻辑

*/

$(function(){

    var data_url = '/query/data';
    $('#condition_desc').html(context.condition_desc);
    var aLengthMenu = [50, 100, 200];
    var pageLength = 100;

    var t = $(document).ready(function(){
        $('#example').DataTable({
            //data: dataSet,
            columns: columns,
            language: language,

            columnDefs: [
                {
                    "targets": 0,
                    "data": null,
                    "data": null,
                    "className": 'column-bold',
                    "render": function(data, type, row, meta) {
                        return meta.settings._iDisplayStart + meta.row + 1;  //行号
                    },
                    "orderable": false
                },
            ],

            searching: false,                        //去掉搜索框
            bSort: false,                            //禁止排序
            info: false,                             //去掉底部文字
            aLengthMenu: aLengthMenu,                //展示100行
            bLengthChange: false,                    //不显示行选项

            bProcessing : true,                      //必须加上这个才能显示加载中的效果

            // 分页开始
            retrieve: true,
            paging: true,
            ordering: false,
            info: true,
            autoWidth: false,
            pageLength: pageLength,      //每页显示25条数据
            pagingType: "full_numbers", //分页样式：simple, simple_numbers, full, full_numbers，
            bFilter: false, //去掉搜索框方法
            bLengthChange: true,//也就是页面上确认是否可以进行选择一页展示多少条
            serverSide: true, //启用服务器端分页，要进行后端分页必须的环节

            ajax: function (data, callback, settings) {
                //封装相应的请求参数，这里获取页大小和当前页码
                var pagesize = data.length;  //页面显示记录条数，在页面显示每页显示多少项的时候,页大小
                var start = data.start;  //开始的记录序号
                var page = (data.start) / data.length + 1;  //当前页码
                var data = {
                    page: page,
                    pagesize: pagesize,  //这里只传了当前页和页大小，如果有其他参数，可继续封装
                    context: context,
                }
                var post_body = JSON.stringify(data);

                //console.log(post_body);

                $.ajax({
                    type: "POST",
                    contentType: "application/json;charset=utf-8",
                    url: data_url,
                    cache : false,                    //禁用缓存
                    data: post_body,                  //传入已封装的参数
                    dataType: "json",                 //返回数据格式为json
                    success: function(data) {

//                        console.log("============数据==========")
//                        console.log(data)

                        var arr = "";
                        if ('object' == typeof data) {
                            arr = data;
                        } else {
                            arr = $.parseJSON(data);                              //将json字符串转化为了一个Object对象
                        }

                        if (arr.result.error) {
                            alert_msg(arr.result.msg);
                            return;
                        }

                        var returnData = {};
//                        returnData.draw = arr.result.data_set.pageCount;        //这里直接自行返回了draw计数器,应该由后台返回，没什么卵用！
                        returnData.recordsTotal = arr.result.total_count;         //totalCount指的是总记录数
                        returnData.recordsFiltered = arr.result.total_count;      //后台不实现过滤功能,全部的记录数都需输出到前端，记录数为总数
                        returnData.data = arr.result.data_set;                    //返回数据
                        callback(returnData);                                     //这个别忘了！！！
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
                        alert_msg("查询失败");
                        $wrapper.spinModal(false);
                    }
                });
            },
        });
    });

})