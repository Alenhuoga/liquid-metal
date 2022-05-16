$(function(){

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




    /* =比例饼状图=*/
    var professionrate = echarts.init(document.getElementById('professionrate'));
    option = {
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            right: '0',
            y:'middle',
            textStyle:{
                color:"#fff"
            },
            data: ['Ga','In','Al','Fe','Co','Ni',
                'Cu','Zn','Mg','Ag','Bi','Sn',
            ],
            formatter:function(name){
                var oa = option.series[0].data;
                var num = oa[0].value + oa[1].value + oa[2].value;
                for(var i = 0; i < option.series[0].data.length; i++){
                    if(name==oa[i].name){
                        return name +  ' '+oa[i].value;
                    }
                }
            }
        },
        series : [
            {
                name: '该元素所占比例',
                type: 'pie',
                radius : '50%',
                center: ['40%', '50%'],
                data:[
                    {value:0, name:'Ga'},
                    {value:0, name:'In'},
                    {value:0, name:'Al'},

                    {value:0, name:'Fe'},
                    {value:0, name:'Co'},
                    {value:0, name:'Ni'},

                    {value:0, name:'Cu'},
                    {value:0, name:'Zn'},
                    {value:0, name:'Mg'},

                    {value:0, name:'Ag'},
                    {value:0, name:'Bi'},
                    {value:0, name:'Sn'},
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },
                itemStyle: {
                    normal: {
                        label:{
                            show: true,
                            position:'outside',
                            formatter: '  {b}'
                        }
                    },
                    labelLine :{show:true}
                }
            }
        ]
    };
    professionrate.setOption(option);


    /*标准*/
    var radar = echarts.init(document.getElementById('radar'));

    option = {
        title: {
            text: ''
        },
        tooltip: {},
        legend: {

            data: ['LSTM', 'model 2','model 3'],
            x:"center",
            y:'bottom',
            textStyle:{
                color:"#fff"
            }
        },
        color: ['#4c95d9', '#f6731b', '#8cd43f'],
        radar: {
            name:{
                textStyle: {
                    //设置颜色
                    color:'#fff'
                }
            },
            indicator: [
                { name: '粘度', max: 0.06},
                { name: '密度', max: 10},
                { name: '热导率', max: 100},
                { name: '导电率', max: 11600000},
                { name: '硬度', max: 20},

            ],
            center: ['50%','50%'],
            radius: "58%"
        },
        series: [{
            name: '',
            type: 'radar',
            itemStyle : {
                normal : {
                    splitLine: {
                        lineStyle: {

                        }
                    },
                    label: {
                        show: false,
                        textStyle:{
                        },
                        formatter:function(params) {
                            return params.value;}
                    },
                }
            },
            data : [
                {
                    value : [],
                    name : 'LSTM'
                },
                {
                    value : [],
                    name : 'model 2'
                },
                {
                    value : [],
                    name : 'model 3'
                }
            ]
        }]
    };
    radar.setOption(option);



            /* 比例变化*/
    var changedetail = echarts.init(document.getElementById('changedetail'));
    option = {
        tooltip: {
            trigger: 'axis',
            formatter: '{b}</br>{a}: {c}</br>{a1}: {c1}'
        },
        toolbox: {
            show:false,
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data:['',''],
            show:false
        },
        grid:{
            top:'18%',
            right:'5%',
            bottom:'8%',
            left:'5%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: ['Mg','Al','Fe','Co','Ni','Cu','Zn','Ga','Ag','In','Sn','Bi'],
                splitLine:{
                    show:false,
                    lineStyle:{
                        color: '#3c4452'
                    }
                },
                axisTick: {
                    show: false
                },
                axisLabel:{
                    textStyle:{
                        color:"#fff"
                    },
                    lineStyle:{
                        color: '#519cff'
                    },
                    alignWithLabel: true,
                    interval:0
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '百分比',
                nameTextStyle:{
                    color:'#fff'
                },
                interval: 10,
                max:100,
                min: 0,
                splitLine:{
                    show:true,
                    lineStyle:{
                        color: '#23303f'
                    }
                },
                axisLine: {
                    show:false,
                    lineStyle: {
                        color: '#115372'
                    }
                },
                axisTick: {
                    show: false
                },
                axisLabel:{
                    textStyle:{
                        color:"#fff"
                    },
                    alignWithLabel: true,
                    interval:0

                }
            },
            {
                min: 0,
                max: 1,
                interval: 0.2,
                type: 'value',
                name: '分数',
                nameTextStyle:{
                    color:'#fff'
                },
                splitLine:{
                    show:true,
                    lineStyle:{
                        color: '#23303f'
                    }
                },
                axisLine: {
                    show:false,
                    lineStyle: {
                        color: '#115372'
                    }
                },
                axisTick: {
                    show: false
                },
                axisLabel:{
                    textStyle:{
                        color:"#fff"
                    },
                    alignWithLabel: true,
                    interval:0

                }
            }
        ],
        color:"yellow",
        series: [
            {
                name:'百分比',
                type:'bar',



                data:[0, 0, 0, 0, 0,0, 0, 0, 0, 0,0,0],


                boundaryGap: '45%',
                barWidth:'40%',

                itemStyle: {
                    normal: {
                        color: function(params) {
                            var colorList = [
                                '#6bc0fb','#7fec9d','#fedd8b','#ffa597',
                                '#84e4dd', '#6bc0fb','#7fec9d','#fedd8b',
                                '#ffa597','#84e4dd', '#6bc0fb','#7fec9d',
                            ];
                            return colorList[params.dataIndex]
                        },label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}'
                        }
                    }
                }
            },

            {
                name:'分数制',
                type:'line',
                yAxisIndex: 1,
                lineStyle: {
                    normal: {
                        color:'#c39705'
                    }
                },



                data:[0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
            }
        ]
    };
    changedetail.setOption(option);



    	$("#button_predict").click(function(){
    	    var num_body ={"Ga":$('#Ga').val(),"In":$('#In').val(),"Al":$('#Al').val(),"Fe":$('#Fe').val(),
            "Co":$('#Co').val(),"Ni":$('#Ni').val(),"Cu":$('#Cu').val(),"Zn":$('#Zn').val(),
            "Mg":$('#Mg').val(),"Ag":$('#Ag').val(),"Bi":$('#Bi').val(),"Sn":$('#Sn').val()
            }

            console.log(JSON.stringify(num_body))
            num_body = JSON.stringify(num_body)



   $.ajax({
        url: "/post/",
        type: "POST",        //请求类型
        data: num_body,


       ContentType:'application/json',
       headers:{'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
       success: function (data,status) {
            //当请求执行完成后，自动调用
           //将字符串解析为JSON
            var data = JSON.parse(data)

            console.log(data["viscosity"])
            console.log(typeof (data["viscosity"]))

            alert("数据: \n" + data + "\n状态: " + status);
            option = {
        title: {
            text: ''
        },
        tooltip: {},
        legend: {

            data: ['LSTM', 'model 2','model 3'],
            x:"center",
            y:'bottom',
            textStyle:{
                color:"#fff"
            }
        },
        color: ['#4c95d9', '#f6731b', '#8cd43f'],
        radar: {
            name:{
                textStyle: {
                    //设置颜色
                    color:'#fff'
                }
            },
            indicator: [
                { name: '粘度', max: 0.06},
                { name: '密度', max: 10},
                { name: '热导率', max: 100},
                { name: '导电率', max: 11600000},
                { name: '硬度', max: 20},


            ],
            center: ['50%','50%'],
            radius: "58%"
        },
        series: [{
            name: '',
            type: 'radar',
            itemStyle : {
                normal : {
                    splitLine: {
                        lineStyle: {

                        }
                    },
                    label: {
                        show: false,
                        textStyle:{
                        },
                        formatter:function(params) {
                            return params.value;}
                    },
                }
            },
            data : [
                {
                    value : [data["viscosity"],data["density"],data["heat_conductivitys"],data["conductivity"],data["solidity"]],
                    name : 'LSTM'
                },
                {
                    value : [12,13,22],
                    name : 'model 2'
                },
                {
                    value :  [12,13,22],
                    name : 'model 3'
                }
            ]
        }]
    };
    radar.setOption(option);


    //饼状图渲染
    option = {
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            right: '0',
            y:'middle',
            textStyle:{
                color:"#fff"
            },
            data: ['Ga','In','Al','Fe','Co','Ni',
                'Cu','Zn','Mg','Ag','Bi','Sn',
            ],
            formatter:function(name){
                var oa = option.series[0].data;
                var num = oa[0].value + oa[1].value + oa[2].value;
                for(var i = 0; i < option.series[0].data.length; i++){
                    if(name==oa[i].name){
                        return name +  ' '+oa[i].value;
                    }
                }
            }
        },
        series : [
            {
                name: '该元素所占比例',
                type: 'pie',
                radius : '50%',
                center: ['40%', '50%'],
                data:[
                    {value:parseFloat($('#Ga').val()), name:'Ga'},
                    {value:parseFloat($('#In').val()), name:'In'},
                    {value:parseFloat($('#Al').val()), name:'Al'},

                    {value:parseFloat($('#Fe').val()), name:'Fe'},
                    {value:parseFloat($('#Co').val()), name:'Co'},
                    {value:parseFloat($('#Ni').val()), name:'Ni'},

                    {value:parseFloat($('#Cu').val()), name:'Cu'},
                    {value:parseFloat($('#Zn').val()), name:'Zn'},
                    {value:parseFloat($('#Mg').val()), name:'Mg'},

                    {value:parseFloat($('#Ag').val()), name:'Ag'},
                    {value:parseFloat($('#Bi').val()), name:'Bi'},
                    {value:parseFloat($('#Sn').val()), name:'Sn'},
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },
                itemStyle: {
                    normal: {
                        label:{
                            show: true,
                            position:'outside',
                            formatter: '  {b}'
                        }
                    },
                    labelLine :{show:true}
                }
            }
        ]
    };
    professionrate.setOption(option);


    $("#density").empty()
    $("#density").append("密度："+data["density"])

    $("#solidity").empty()
    $("#solidity").append("硬度："+data["solidity"])

    $("#viscosity").empty()
    $("#viscosity").append("粘度："+data["viscosity"])

    $("#heat_conductivitys").empty()
    $("#heat_conductivitys").append("热导率："+data["heat_conductivitys"])

    $("#conductivity").empty()
    $("#conductivity").append("电导率："+data["conductivity"])


    option = {
        tooltip: {
            trigger: 'axis',
            formatter: '{b}</br>{a}: {c}</br>{a1}: {c1}'
        },
        toolbox: {
            show:false,
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data:['',''],
            show:false
        },
        grid:{
            top:'18%',
            right:'5%',
            bottom:'8%',
            left:'5%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: ['Mg','Al','Fe','Co','Ni','Cu','Zn','Ga','Ag','In','Sn','Bi'],
                splitLine:{
                    show:false,
                    lineStyle:{
                        color: '#3c4452'
                    }
                },
                axisTick: {
                    show: false
                },
                axisLabel:{
                    textStyle:{
                        color:"#fff"
                    },
                    lineStyle:{
                        color: '#519cff'
                    },
                    alignWithLabel: true,
                    interval:0
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '百分比',
                nameTextStyle:{
                    color:'#fff'
                },
                interval: 10,
                max:100,
                min: 0,
                splitLine:{
                    show:true,
                    lineStyle:{
                        color: '#23303f'
                    }
                },
                axisLine: {
                    show:false,
                    lineStyle: {
                        color: '#115372'
                    }
                },
                axisTick: {
                    show: false
                },
                axisLabel:{
                    textStyle:{
                        color:"#fff"
                    },
                    alignWithLabel: true,
                    interval:0

                }
            },
            {
                min: 0,
                max: 1,
                interval: 0.2,
                type: 'value',
                name: '分数',
                nameTextStyle:{
                    color:'#fff'
                },
                splitLine:{
                    show:true,
                    lineStyle:{
                        color: '#23303f'
                    }
                },
                axisLine: {
                    show:false,
                    lineStyle: {
                        color: '#115372'
                    }
                },
                axisTick: {
                    show: false
                },
                axisLabel:{
                    textStyle:{
                        color:"#fff"
                    },
                    alignWithLabel: true,
                    interval:0

                }
            }
        ],
        color:"yellow",
        series: [
            {
                name:'百分比',
                type:'bar',



                data:[0, 0, 0, 0, 0,0, 0, 0, 0, 0,0,0],


                boundaryGap: '45%',
                barWidth:'40%',

                itemStyle: {
                    normal: {
                        color: function(params) {
                            var colorList = [
                                '#6bc0fb','#7fec9d','#fedd8b','#ffa597',
                                '#84e4dd', '#6bc0fb','#7fec9d','#fedd8b',
                                '#ffa597','#84e4dd', '#6bc0fb','#7fec9d',
                            ];
                            return colorList[params.dataIndex]
                        },label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}'
                        }
                    }
                }
            },

            {
                name:'分数制',
                type:'line',
                yAxisIndex: 1,
                lineStyle: {
                    normal: {
                        color:'#c39705'
                    }
                },



                data:[0.1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
            }
        ]
    };
    changedetail.setOption(option);







            Ga = $('#Ga').val()
            In = $('#In').val()
            Al = $('#Al').val()
            Fe = $('#Fe').val()
            Co =$('#Co').val()
            Ni = $('#Ni').val()
            Cu = $('#Cu').val()
            Zn = $('#Zn').val()
            Mg = $('#Mg').val()
            Ag = $('#Ag').val()
            Bi = $('#Bi').val()
            Sn = $('#Sn').val()



    option = {
        tooltip: {
            trigger: 'axis',
            formatter: '{b}</br>{a}: {c}</br>{a1}: {c1}'
        },
        toolbox: {
            show:false,
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data:['',''],
            show:false
        },
        grid:{
            top:'18%',
            right:'5%',
            bottom:'8%',
            left:'5%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: ['Mg','Al','Fe','Co','Ni','Cu','Zn','Ga','Ag','In','Sn','Bi'],
                splitLine:{
                    show:false,
                    lineStyle:{
                        color: '#3c4452'
                    }
                },
                axisTick: {
                    show: false
                },
                axisLabel:{
                    textStyle:{
                        color:"#fff"
                    },
                    lineStyle:{
                        color: '#519cff'
                    },
                    alignWithLabel: true,
                    interval:0
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '百分比',
                nameTextStyle:{
                    color:'#fff'
                },
                interval: 10,
                max:100,
                min: 0,
                splitLine:{
                    show:true,
                    lineStyle:{
                        color: '#23303f'
                    }
                },
                axisLine: {
                    show:false,
                    lineStyle: {
                        color: '#115372'
                    }
                },
                axisTick: {
                    show: false
                },
                axisLabel:{
                    textStyle:{
                        color:"#fff"
                    },
                    alignWithLabel: true,
                    interval:0

                }
            },
            {
                min: 0,
                max: 1,
                interval: 0.2,
                type: 'value',
                name: '分数',
                nameTextStyle:{
                    color:'#fff'
                },
                splitLine:{
                    show:true,
                    lineStyle:{
                        color: '#23303f'
                    }
                },
                axisLine: {
                    show:false,
                    lineStyle: {
                        color: '#115372'
                    }
                },
                axisTick: {
                    show: false
                },
                axisLabel:{
                    textStyle:{
                        color:"#fff"
                    },
                    alignWithLabel: true,
                    interval:0

                }
            }
        ],
        color:"yellow",
        series: [
            {
                name:'百分比',
                type:'bar',



                data:[Mg,Al,Fe,Co,Ni, Cu , Zn ,Ga , Ag , In , Sn , Bi ],


                boundaryGap: '45%',
                barWidth:'40%',

                itemStyle: {
                    normal: {
                        color: function(params) {
                            var colorList = [
                                '#6bc0fb','#7fec9d','#fedd8b','#ffa597',
                                '#84e4dd', '#6bc0fb','#7fec9d','#fedd8b',
                                '#ffa597','#84e4dd', '#6bc0fb','#7fec9d',
                            ];
                            return colorList[params.dataIndex]
                        },label: {
                            show: true,
                            position: 'top',
                            formatter: '{c}'
                        }
                    }
                }
            },

            {
                name:'分数制',
                type:'line',
                yAxisIndex: 1,
                lineStyle: {
                    normal: {
                        color:'#c39705'
                    }
                },



                data:[Mg/100,Al/ 100,Fe/ 100,Co/ 100,Ni/ 100, Cu/ 100 , Zn/ 100 ,Ga/ 100 , Ag/ 100 , In/ 100 , Sn/ 100 , Bi/ 100 ]
            }
        ]
    };
    changedetail.setOption(option);


        },







        error: function () {
            //当请求错误之后，自动调用
        }
    });

	});






    /* 飞鸟尽*/
    var graduateyear = echarts.init(document.getElementById('graduateyear'));
    option = {
        title : {
            text:"",
            x:'center',
            y:'top',
            textStyle:
            {
                color:'#fff',
                fontSize:13
            }
        },
        tooltip : {
            trigger: 'axis'
        },
        grid: {
            left: '3%',
            right: '8%',
            bottom: '5%',
            top:"13%",
            containLabel: true
        },
        color:["#72b332",'#35a9e0'],
        legend: {
            data:['test1','test2'],
            show:true,

            right:'15%',
            y:"0",
            textStyle:{
                color:"#999",
                fontSize:'13'
            },
        },
        toolbox: {
            show : false,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : ['2022年','2023年','2024年','2025年','2026年','2027年','2028年'],
                splitLine:{
                    show:true,
                    lineStyle:{
                        color: '#2d3b53'
                    }
                },
                axisLabel:{
                    textStyle:{
                        color:"#fff"
                    },
                    alignWithLabel: true,
                    interval:0,
                    rotate:'15'
                }
            }
        ],
        yAxis : [
            {
                type : 'value',
                splitLine:{
                    show:true,
                    lineStyle:{
                        color: '#2d3b53'
                    }
                },
                axisLabel:{
                    textStyle:{
                        color:"#999"
                    }
                },
            }
        ],
        series : [
            {
                name:'test1',
                type:'line',
                smooth:true,
                symbol:'roundRect',
                data:[1168,1189,1290,1300,1345,1256,1045]
            },
            {
                name:'test2',
                type:'line',
                smooth:true,
                symbol:'roundRect',
                data:[1234,1290,1311,1145,1045,900,673]
            }
        ]
    };
    graduateyear.setOption(option);


})