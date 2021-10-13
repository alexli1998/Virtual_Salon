function upload_img() {
    var formData = new FormData();
        formData.append('file', $("#upload_img")[0].files[0]);
//        alert(formData.get('file').name)
        $.ajax({
                url: '/upload_img',
                type: 'post',
                data: formData,
                processData: false,
                contentType: false,
                dataType: 'text',
                success: function() {
                    $.getJSON('/upload_img', {'img': '' + formData.get('file').name}, function(response) {
                        document.getElementById('userimg').src = response.url
                    });
                },
                error: function(response) {

                }
        });

}

$(function() {
    $("#recommend").click(function (event) {
        $.getJSON('/get_recommendation', { }, function(response) {
            document.getElementById('userimg').src = response.url
        });
    });
});



//function upload_img()
//{
//    var SqlQuery = "select * from inventory";
//    var rs = new ActiveXObject("ADODB.Recordset");
//    rs.open(SqlQuery, connection);
//
//    var result="";
//    while(!rs.eof)
//        {
//            result+=rs.Fields("product")+'\t'+rs.Fields("quantity")+'<br/>';
//            rs.moveNext();
//        }
//    document.getElementById("INVENTORY").innerHTML = result;
//}
//
//function getOrder()
//{
//    //初始化
//    var orderString;
//    var lines;
//    var result="";
//
//    orderString = document.getElementById('ORDER').value;
//    matchOrder(orderString,lines,result);
//}
//
//function matchOrder(orderString,lines,result)
//{
//    lines=orderString.split('\n');
//
//    //查询                        
//    var i;
//    for (i = 0; i < lines.length; i++) 
//        {
//            var record=lines[i].split(" ");
//            var SqlQuery = "select * from inventory where product='"+record[0]+"'";
//            var rs = new ActiveXObject("ADODB.Recordset");
//            rs.open(SqlQuery, connection);
//            if(!rs.eof)
//            {
//                var quantity=rs.Fields("quantity");
//
//                var temp=parseInt(quantity)-parseInt(record[1]);
//
//                if(temp>=0)//判断库存能否满足订单
//                {
//                    result+=record[0]+'\t'+record[1]+"仓"+'<br/>';
//                }
//                else
//                {
//                    result+=record[0]+'\t'+record[1]+"买"+'<br/>';
//                }
//            }
//            else
//                result+=record[0]+'\t'+record[1]+'<br/>';
//        }    
//    document.getElementById("OUTPUT").innerHTML = result;
//}


