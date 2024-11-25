<!-- src/components/AirQualityCharts1m.vue -->
<template>
  <div class="charts-container">
    <h1>室内空气质量监测折线图 - 近1分钟</h1>
    <!-- 导航栏组件，当前视图设为 '1m' -->
    <NavigationBar :currentView="'1m'" />

    <!-- 甲醛图表容器，条件应用预警样式 -->
    <div class="charts" :class="{ warning: isWarning }">
      <div class="chart" ref="formaldehydeChart"></div>
      <div class="latest-data">实时甲醛浓度: {{ latestData.formaldehyde_concentration }} mg/m³</div>
      <div v-if="isWarning" class="warning-text">甲醛浓度超标！</div>
    </div>

    <!-- 温度图表容器 -->
    <div class="charts">
      <div class="chart" ref="temperatureChart"></div>
      <div class="latest-data">实时温度: {{ latestData.temperature }} °C</div>
    </div>

    <!-- 湿度图表容器 -->
    <div class="charts">
      <div class="chart" ref="humidityChart"></div>
      <div class="latest-data">实时湿度: {{ latestData.humidity }} %</div>
    </div>

    <!-- CO₂浓度图表容器 -->
    <div class="charts">
      <div class="chart" ref="co2Chart"></div>
      <div class="latest-data">实时CO₂浓度: {{ latestData.co2_concentration }} ppm</div>
    </div>

    <!-- PM2.5浓度图表容器 -->
    <div class="charts">
      <div class="chart" ref="pm25Chart"></div>
      <div class="latest-data">实时PM2.5浓度: {{ latestData.pm25_concentration }} µg/m³</div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'; // 导入ECharts库
import axios from 'axios'; // 导入axios库，用于发送HTTP请求
import NavigationBar from './NavigationBar.vue'; // 导入导航栏组件

export default {
  name: 'AirQualityCharts1m',
  components: {
    NavigationBar // 注册导航栏组件
  },
  data() {
    return {
      airQualityData: [], // 存储空气质量数据的数组
      filteredData: [], // 存储过滤后的空气质量数据
      latestData: { // 存储最新的空气质量数据
        co2_concentration: 0,
        pm25_concentration: 0,
        formaldehyde_concentration: 0,
        temperature: 0,
        humidity: 0
      },
      charts: {}, // 存储图表实例
      chartStates: {}, // 缓存图表状态
      formaldehydeWarningValue: 0.05, // 甲醛浓度预警值
      isWarning: false, // 预警状态
      warningInterval: null // 预警动画间隔
    };
  },
  methods: {
    fetchData() {
      // 从后端获取空气质量数据
      axios.get('http://localhost:8080/api/airquality/data')
          .then(response => {
            this.airQualityData = response.data; // 将响应数据存储到airQualityData
            this.updateCharts(); // 更新图表数据
          })
          .catch(error => {
            console.error('获取数据时出错!', error);
          });
    },
    updateCharts() {
      const now = new Date(); // 当前时间
      const range = 1 * 60 * 1000; // 1分钟的毫秒数
      // 过滤最近1分钟的数据
      this.filteredData = this.airQualityData.filter(data => {
        return now - new Date(data.timestamp) <= range;
      });

      // 获取最新的数据点
      this.latestData = this.filteredData[this.filteredData.length - 1] || this.latestData;
      this.initCharts(); // 初始化或更新图表
      this.checkFormaldehydeWarning(); // 检查甲醛预警
    },
    initCharts() {
      // 提取数据的时间戳和各项数据值
      const timestamps = this.filteredData.map(data => data.timestamp);
      const co2 = this.filteredData.map(data => data.co2_concentration);
      const pm25 = this.filteredData.map(data => data.pm25_concentration);
      const formaldehyde = this.filteredData.map(data => data.formaldehyde_concentration);
      const temperature = this.filteredData.map(data => data.temperature);
      const humidity = this.filteredData.map(data => data.humidity);

      // 初始化各个图表
      this.initChart(this.$refs.co2Chart, 'CO₂浓度 (ppm)', timestamps, co2, '#3398DB', 'co2Chart');
      this.initChart(this.$refs.pm25Chart, 'PM2.5浓度 (µg/m³)', timestamps, pm25, '#FF5733', 'pm25Chart');
      this.initChart(this.$refs.formaldehydeChart, '甲醛浓度 (mg/m³)', timestamps, formaldehyde, '#33FF57', 'formaldehydeChart', this.formaldehydeWarningValue);
      this.initChart(this.$refs.temperatureChart, '温度 (°C)', timestamps, temperature, '#FF33A6', 'temperatureChart');
      this.initChart(this.$refs.humidityChart, '湿度 (%)', timestamps, humidity, '#33C4FF', 'humidityChart');
    },
    initChart(container, title, timestamps, data, color, chartKey, warningValue = null) {
      // 初始化或更新图表
      if (!this.charts[chartKey]) {
        this.charts[chartKey] = echarts.init(container);
      } else {
        const chartState = this.chartStates[chartKey];
        if (chartState) {
          this.charts[chartKey].setOption(chartState.option, false);
          this.charts[chartKey].dispatchAction(chartState.action);
        }
      }

      // 配置图表选项
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
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: '#ddd'
            }
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
            },
            // 如果存在预警值，添加标线
            markLine: warningValue ? {
              silent: true,
              data: [
                {
                  yAxis: warningValue,
                  lineStyle: {
                    color: 'red'
                  },
                  label: {
                    formatter: '' + warningValue + ' mg/m³',
                    position: 'end'
                  }
                }
              ]
            } : {}
          }
        ]
      };

      this.charts[chartKey].setOption(option);

      // 缓存图表状态
      this.chartStates[chartKey] = {
        option: this.charts[chartKey].getOption(),
        action: { type: 'dataZoom', start: 0, end: 100 }
      };
    },
    checkFormaldehydeWarning() {
      // 检查最新甲醛浓度是否超标
      const formaldehyde = this.latestData.formaldehyde_concentration;
      if (formaldehyde > this.formaldehydeWarningValue) {
        this.triggerWarning();
      } else {
        this.clearWarning();
      }
    },
    triggerWarning() {
      // 启动预警动画
      if (!this.isWarning) {
        this.isWarning = true;
        this.warningInterval = setInterval(() => {
          this.$refs.formaldehydeChart.style.animation =
              this.$refs.formaldehydeChart.style.animation === '' ? 'warning-bg 1s infinite' : '';
        }, 1000);
      }
    },
    clearWarning() {
      // 清除预警动画
      if (this.isWarning) {
        clearInterval(this.warningInterval);
        this.$refs.formaldehydeChart.style.animation = '';
        this.isWarning = false;
      }
    }
  },
  mounted() {
    this.fetchData(); // 组件挂载时获取数据
    setInterval(this.fetchData, 10000); // 每10秒请求一次数据
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
  position: relative;
}
.charts.warning {
  animation: warning-bg 1s infinite;
}
.chart {
  width: 100%;
  height: 300px;
}
.latest-data {
  width: 25%;
  padding-left: 20px;
  font-size: 1.2em;
  text-align: left;
}
.warning-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5em;
  color: red;
  animation: warning-text-blink 1s infinite;
}
@keyframes warning-bg {
  0% { background-color: transparent; }
  50% { background-color: rgba(255, 0, 0, 0.44); }
  100% { background-color: transparent; }
}
@keyframes warning-text-blink {
  0% { opacity: 1; }
  50% { opacity: 0; }
  100% { opacity: 1; }
}
</style>
