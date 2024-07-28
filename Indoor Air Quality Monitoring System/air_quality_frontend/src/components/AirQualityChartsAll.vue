<template>
  <div class="charts-container">
    <h1>室内空气质量监测折线图 - 近1小时</h1>
    <NavigationBar :currentView="'all'" @navigate="handleNavigate" />
    <div class="chart-container">
      <h1>室内空气质量监测折线图</h1>
      <div ref="chart" class="chart"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import NavigationBar from './NavigationBar.vue';

export default {
  name: 'AirQualityChart1h',
  components: {
    NavigationBar
  },
  data() {
    return {
      airQualityData: [],
    };
  },
  methods: {
    fetchData() {
      axios.get('http://localhost:8080/api/airquality/data')
          .then(response => {
            this.airQualityData = response.data;
            this.initChart();
          })
          .catch(error => {
            console.error('There was an error!', error);
          });
    },
    initChart() {
      const chart = echarts.init(this.$refs.chart);
      const timestamps = this.airQualityData.map(data => data.timestamp);
      const co2 = this.airQualityData.map(data => data.co2_concentration);
      const pm25 = this.airQualityData.map(data => data.pm25_concentration);
      const formaldehyde = this.airQualityData.map(data => data.formaldehyde_concentration);
      const temperature = this.airQualityData.map(data => data.temperature);
      const humidity = this.airQualityData.map(data => data.humidity);

      const option = {
        tooltip: {
          trigger: 'axis',
        },
        legend: {
          data: ['CO₂浓度', 'PM2.5浓度', '甲醛浓度', '温度', '湿度']
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: timestamps
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'CO₂浓度',
            type: 'line',
            data: co2
          },
          {
            name: 'PM2.5浓度',
            type: 'line',
            data: pm25
          },
          {
            name: '甲醛浓度',
            type: 'line',
            data: formaldehyde
          },
          {
            name: '温度',
            type: 'line',
            data: temperature
          },
          {
            name: '湿度',
            type: 'line',
            data: humidity
          }
        ]
      };

      chart.setOption(option);
    },
    handleNavigate(view) {
      // Handle navigation logic here
      console.log(`Navigating to ${view}`);
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.chart {
  width: 90%;
  height: 80vh;
}
</style>
