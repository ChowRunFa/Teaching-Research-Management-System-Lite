<template>

  <div className="about">
    <h1>This is an about page</h1>
    <div id="main"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  mounted() {

var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;

option = {
  angleAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  radiusAxis: {},
  polar: {},
  series: [
    {
      type: 'bar',
      data: [1, 2, 3, 4, 3, 5, 1],
      coordinateSystem: 'polar',
      name: 'A',
      stack: 'a',
      emphasis: {
        focus: 'series'
      }
    },
    {
      type: 'bar',
      data: [2, 4, 6, 1, 3, 2, 1],
      coordinateSystem: 'polar',
      name: 'B',
      stack: 'a',
      emphasis: {
        focus: 'series'
      }
    },
    {
      type: 'bar',
      data: [1, 2, 3, 4, 1, 2, 5],
      coordinateSystem: 'polar',
      name: 'C',
      stack: 'a',
      emphasis: {
        focus: 'series'
      }
    }
  ],
  legend: {
    show: true,
    data: ['A', 'B', 'C']
  }
};

option && myChart.setOption(option);


  },
};
</script>


<style>
#main {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80vw; /* Set the width to 80% of the viewport width */
  height: 60vh; /* Set the height to 60% of the viewport height */
}

</style>


<style scoped>

</style>