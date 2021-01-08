<script type="text/javascript">
    //产生一个随机颜色
    var get_random_color = function(){
        return  '#' + (function(color){
             return (color +=  '0123456789abcdef'[Math.floor(Math.random()*16)])
             && (color.length == 6) ?  color : arguments.callee(color);
        })('');
    }

    // 基于准备好的dom，初始化echarts实例
    $.ajax({
      url:"/get_result_api",
      type:"POST",
      success:(data) =>{
          render(JSON.parse(data))

      }
    })
    var render = (slot_info) =>{
        var myChart = echarts.init(document.getElementById('main'));

        var data = [];
        var startTime = +new Date();
        // categories 存放停机位列表
        var categories = []
        for(let i in slot_info){
            categories.push(i)
        }
        var type = []
        for(let i of slot_info){
            for(let j of i){
                let temp_obj = {}
                j.color = get_random_color()
                data.push(j)
            }
        }

        // Generate mock data
        echarts.util.each(categories, function (category, index) {
            var baseTime = startTime;
            for (let type_item of type) {

                var duration = Math.round(Math.random() * 10000);
                data.push({
                    name: typeItem.name,
                    value: [
                        index,
                        new Date(typeItem.entryTime).getTime(),
                        new Date(typeItem.outTime).getTime(),
                        //duration
                    ],
                    itemStyle: {
                        normal: {
                            color: typeItem.color
                        }
                    }
                });
                baseTime += Math.round(Math.random() * 2000);
            }
        });

        function renderItem(params, api) {
            var categoryIndex = api.value(0);
            var start = api.coord([api.value(1), categoryIndex]);
            var end = api.coord([api.value(2), categoryIndex]);
            var height = api.size([0, 1])[1] * 0.6;

            return {
                type: 'rect',
                shape: echarts.graphic.clipRectByRect({
                    x: start[0],
                    y: start[1] - height / 2,
                    width: end[0] - start[0],
                    height: height
                }, {
                    x: params.coordSys.x,
                    y: params.coordSys.y,
                    width: params.coordSys.width,
                    height: params.coordSys.height
                }),
                style: api.style()
            };
        }


        option = {
            tooltip: {
                formatter: function (params) {
                    return params.marker + params.name + ': ' + params.value[1] + ','+params.value[2] + ' ';
                }
            },
            title: {
                text: '',
                left: 'center'
            },
            dataZoom: [{
                type: 'slider',
                filterMode: 'weakFilter',
                showDataShadow: false,
                top: 400,
                height: 10,
                borderColor: 'transparent',
                backgroundColor: '#e2e2e2',
                handleIcon: 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7v-1.2h6.6z M13.3,22H6.7v-1.2h6.6z M13.3,19.6H6.7v-1.2h6.6z', // jshint ignore:line
                handleSize: 20,
                handleStyle: {
                    shadowBlur: 6,
                    shadowOffsetX: 1,
                    shadowOffsetY: 2,
                    shadowColor: '#aaa'
                },
                labelFormatter: ''
            }, {
                type: 'inside',
                filterMode: 'weakFilter'
            }],
            grid: {
                height:300
            },
            xAxis: {
                min: startTime,
                scale: true,
                axisLabel: {
                    formatter: function (val) {
                        return Math.max(0, val - startTime) + ' ms';
                    }
                }
            },
            yAxis: {
                data: categories
            },
            series: [{
                type: 'custom',
                renderItem: renderItem,
                itemStyle: {
                    normal: {
                        opacity: 0.8
                    }
                },
                encode: {
                    x: [1, 2],
                    y: 0
                },
                data: data
            }]
        };
        myChart.setOption(option, true);
    }


</script>
