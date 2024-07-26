<template>
  <div>
    <h1>室内空气质量监测</h1>
    <form @submit.prevent="createData">
      <div>
        <label>时间:</label>
        <input v-model="newData.timestamp" type="datetime-local" required />
      </div>
      <div>
        <label>二氧化碳浓度:</label>
        <input v-model="newData.co2_concentration" type="number" step="0.01" required />
      </div>
      <div>
        <label>PM2.5浓度:</label>
        <input v-model="newData.pm25_concentration" type="number" step="0.01" required />
      </div>
      <div>
        <label>甲醛浓度:</label>
        <input v-model="newData.formaldehyde_concentration" type="number" step="0.01" required />
      </div>
      <div>
        <label>温度:</label>
        <input v-model="newData.temperature" type="number" step="0.01" required />
      </div>
      <div>
        <label>湿度:</label>
        <input v-model="newData.humidity" type="number" step="0.01" required />
      </div>
      <button type="submit">添加数据</button>
    </form>
    <table>
      <thead>
      <tr>
        <th>时间</th>
        <th>二氧化碳浓度</th>
        <th>PM2.5浓度</th>
        <th>甲醛浓度</th>
        <th>温度</th>
        <th>湿度</th>
        <th>操作</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="data in airQualityData" :key="data.id">
        <td>{{ data.timestamp }}</td>
        <td>{{ data.co2_concentration }}</td>
        <td>{{ data.pm25_concentration }}</td>
        <td>{{ data.formaldehyde_concentration }}</td>
        <td>{{ data.temperature }}</td>
        <td>{{ data.humidity }}</td>
        <td>
          <button @click="deleteData(data.id)">删除</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      airQualityData: [],
      newData: {
        timestamp: '',
        co2_concentration: '',
        pm25_concentration: '',
        formaldehyde_concentration: '',
        temperature: '',
        humidity: ''
      }
    };
  },
  methods: {
    fetchData() {
      axios.get('http://localhost:8080/api/airquality/data')
          .then(response => {
            this.airQualityData = response.data;
          })
          .catch(error => {
            console.error('There was an error!', error);
          });
    },
    createData() {
      axios.post('http://localhost:8080/api/airquality/data', this.newData)
          .then(() => {
            this.fetchData();
          })
          .catch(error => {
            console.error('There was an error!', error);
          });
    },
    deleteData(id) {
      axios.delete(`http://localhost:8080/api/airquality/data/${id}`)
          .then(() => {
            this.fetchData();
          })
          .catch(error => {
            console.error('There was an error!', error);
          });
    }
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style scoped>
/* 简单的样式 */
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 8px;
  border: 1px solid #ccc;
}
form {
  margin-bottom: 20px;
}
</style>
