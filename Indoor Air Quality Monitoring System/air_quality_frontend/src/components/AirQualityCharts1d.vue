<!-- src/components/AirQualityCharts1h.vue -->
<template>
  <div class="charts-container">
    <h1>室内空气质量监测折线图 - 近1小时</h1>
    <NavigationBar :currentView="'1d'" />
    <div class="charts">
      <div class="chart" ref="formaldehydeChart"></div>
      <div class="latest-data">实时甲醛浓度: {{ latestData.formaldehyde_concentration }} mg/m³</div>
    </div>
    <div class="charts">
      <div class="chart" ref="temperatureChart"></div>
      <div class="latest-data">实时温度: {{ latestData.temperature }} °C</div>
    </div>
    <div class="charts">
      <div class="chart" ref="humidityChart"></div>
      <div class="latest-data">实时湿度: {{ latestData.humidity }} %</div>
    </div>
    <div class="charts">
      <div class="chart" ref="co2Chart"></div>
      <div class="latest-data">实时CO₂浓度: {{ latestData.co2_concentration }} ppm</div>
    </div>
    <div class="charts">
      <div class="chart" ref="pm25Chart"></div>
      <div class="latest-data">实时PM2.5浓度: {{ latestData.pm25_concentration }} µg/m³</div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
import NavigationBar from './NavigationBar.vue';

export default {
  name: 'AirQualityCharts1h',
  components: {
    NavigationBar
  },
  data() {
    return {
      airQualityData: [],
      filteredData: [],
      latestData: {
        co2_concentration: 0,
        pm25_concentration: 0,
        formaldehyde_concentration: 0,
        temperature: 0,
        humidity: 0
      },
      charts: {},
      chartStates: {} // To cache chart states
    };
  },
  methods: {
    fetchData() {
      axios.get('http://localhost:8080/api/airquality/data')
          .then(response => {
            this.airQualityData = response.data;
            this.updateCharts();
          })
          .catch(error => {
            console.error('There was an error!', error);
          });
    },
    updateCharts() {
      const now = new Date();
      const range = 1 * 60 * 60 * 1000; // 1 hour in milliseconds
      this.filteredData = this.airQualityData.filter(data => {
        return now - new Date(data.timestamp) <= range;
      });

      this.latestData = this.filteredData[this.filteredData.length - 1] || this.latestData;
      this.initCharts();
    },
    initCharts() {
      const timestamps = this.filteredData.map(data => data.timestamp);
      const co2 = this.filteredData.map(data => data.co2_concentration);
      const pm25 = this.filteredData.map(data => data.pm25_concentration);
      const formaldehyde = this.filteredData.map(data => data.formaldehyde_concentration);
      const temperature = this.filteredData.map(data => data.temperature);
      const humidity = this.filteredData.map(data => data.humidity);

      this.initChart(this.$refs.co2Chart, 'CO₂浓度 (ppm)', timestamps, co2, '#3398DB', 'co2Chart');
      this.initChart(this.$refs.pm25Chart, 'PM2.5浓度 (µg/m³)', timestamps, pm25, '#FF5733', 'pm25Chart');
      this.initChart(this.$refs.formaldehydeChart, '甲醛浓度 (mg/m³)', timestamps, formaldehyde, '#33FF57', 'formaldehydeChart');
      this.initChart(this.$refs.temperatureChart, '温度 (°C)', timestamps, temperature, '#FF33A6', 'temperatureChart');
      this.initChart(this.$refs.humidityChart, '湿度 (%)', timestamps, humidity, '#33C4FF', 'humidityChart');
    },
    initChart(container, title, timestamps, data, color, chartKey) {
      if (!this.charts[chartKey]) {
        this.charts[chartKey] = echarts.init(container);
      } else {
        // Restore previous chart state if available
        const chartState = this.chartStates[chartKey];
        if (chartState) {
          this.charts[chartKey].setOption(chartState.option, false);
          this.charts[chartKey].dispatchAction(chartState.action);
        }
      }

      const option = {
        title: {
          text: title,
          left: 'center',
          textStyle: {
            color: color
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: timestamps,
          axisLabel: {
            color: '#333'
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            color: '#333'
          }
        },
        dataZoom: [
          {
            type: 'inside',
            start: 0,
            end: 100
          },
          {
            start: 0,
            end: 100
          }
        ],
        series: [
          {
            name: title,
            type: 'line',
            data: data,
            smooth: true,
            areaStyle: {
              opacity: 0.2
            },
            lineStyle: {
              color: color
            },
            itemStyle: {
              color: color
            }
          }
        ]
      };

      this.charts[chartKey].setOption(option);

      // Cache current chart state
      this.chartStates[chartKey] = {
        option: this.charts[chartKey].getOption(),
        action: { type: 'dataZoom', start: 0, end: 100 }
      };
    }
  },
  mounted() {
    this.fetchData();
    setInterval(this.fetchData, 9000);
  }
};
</script>

<style scoped>
.charts-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  background-color: #f0f8ff;
  border-radius: 8px;
}
.charts {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 10px;
  background-color: #ffffff;
  border: 1px solid #dfe2e5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}
.chart {
  width: 70%;
  height: 300px;
}
.latest-data {
  width: 25%;
  padding-left: 20px;
  font-size: 1.2em;
  text-align: left;
}
</style>
