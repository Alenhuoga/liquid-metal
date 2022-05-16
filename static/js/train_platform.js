$(function (){

    //跨站伪造
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


$('#test').click(function (){
    $.ajax({
        url:'/train/test/',
        type:"POST",
        data:JSON.stringify({
            model_name:$("#select-model").val()
        }),

        success:function (data,status){

            console.log($("#select-model").val())
            alert("数据: \n" + data + "\n状态: " + status);
            data = JSON.parse(data)
            var len = data["preds"].length
            console.log(len)
            $('#test_result').empty();

            for(i=0;i<len;i++){

            $('#test_result').append("<p>预测的密度是:"+data["preds"][i]+"</p>");
            $('#test_result').append("<p>真实的密度是:"+data["lables"][i]+"</p>");
            }

             $('#test_result').append("<p>R2为:"+data["R2"]+"</p>");
            $('#test_result').append("<p>测试集总的loss为:"+data["M_loss"]+"</p>");
        }

    })

})


var switch_on = true


// #轮询监控控制台日志
var i = setInterval(function (){
    $.ajax({
        url:'/train/test/get/',
        type:'GET',

        success:function (data,status){
            // alert("数据: \n" + data + "\n状态: " + status);
            data = JSON.parse(data)
            console.log(data)
            if (data['log'].length!=0){
            //更新训练日志
            $('#test_result').empty();
            $('#test_result').append(data['log']);

            //更新训练次数
            $('#epoch').empty().append('迭代总次数：'+data['epoch']);

            //更新时间
            $('#train_time').empty().append('训练总耗时：'+data['time']+'秒');


            //更新数据
            $('#data_num').empty().append('训练数据量：'+data['data_num']);
            }



            else {

                console.log(222)
            }

        }


    })
},3000)

$('#train').click(


    function (){

      $('#test_result').empty();
      $('#test_result').append("正在加载模型和准备数据集，准备开始训练.........");

        $.ajax({
        url:'/train/test/density/',
        type:'GET',


        // 成功结束，收到后端的return返回值后 执行
        success:function (data,status){
            alert("训练结束： \n" + data + "\n状态: " + status);
            data = JSON.parse(data)

            if (data.length!=0){
            $('#test_result').empty();
            $('#test_result').append(data);
            }
            else {
                console.log(222)
            }

        }


    })



})


$('#fin_train').click(

    function (){
         alert("关闭训练");
         // clearInterval(i)
        $.ajax({
            url:"/get/",
            type:"POST",
            ContentType:'application/json',
            headers:{'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},

            //传送训练结束指令
            data: JSON.stringify({

               switch:false
            },),

            success:function (){
                console.log('data:'+this.data)
            }



        })
    }
)


$('#backup').click(
    function (){

        $.ajax({
            url:'/backup/',
            type:'GET',

            success:function (data,status){
                alert('数据：'+data+'\n'+'状态'+status)

            }
        })
    }

)

$(".model_history").click(
    function (){

        var model_name = $(this).text()
        alert('成功加载模型：'+$(this).text())
        $.ajax({
            type:'POST',
            url:'/load/',
            data:JSON.stringify({
                'model':model_name
            }),

            success:function (data,staus){
                // alert($(this).text())
            }
        })

    }
)


})



