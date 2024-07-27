<template>
  <!-- 这是 Vue 组件的模板部分 -->
  <div>
    <!-- 标题 -->
    <h1>室内空气质量监测</h1>

    <!-- 表单用于提交新的数据 -->
    <form @submit.prevent="createData">
      <!-- 时间输入 -->
      <div>
        <label>时间:</label>
        <input v-model="newData.timestamp" type="datetime-local" required />
      </div>
      <!-- 二氧化碳浓度输入 -->
      <div>
        <label>二氧化碳浓度:</label>
        <input v-model="newData.co2_concentration" type="number" step="0.01" required />
      </div>
      <!-- PM2.5浓度输入 -->
      <div>
        <label>PM2.5浓度:</label>
        <input v-model="newData.pm25_concentration" type="number" step="0.01" required />
      </div>
      <!-- 甲醛浓度输入 -->
      <div>
        <label>甲醛浓度:</label>
        <input v-model="newData.formaldehyde_concentration" type="number" step="0.01" required />
      </div>
      <!-- 温度输入 -->
      <div>
        <label>温度:</label>
        <input v-model="newData.temperature" type="number" step="0.01" required />
      </div>
      <!-- 湿度输入 -->
      <div>
        <label>湿度:</label>
        <input v-model="newData.humidity" type="number" step="0.01" required />
      </div>
      <!-- 提交按钮 -->
      <button type="submit">添加数据</button>
    </form>

    <!-- 数据展示表格 -->
    <table>
      <thead>
      <tr>
        <!-- 表头 -->
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
      <!-- 使用 v-for 指令遍历 airQualityData 数组 -->
      <tr v-for="data in airQualityData" :key="data.id">
        <!-- 显示数据 -->
        <td>{{ data.timestamp }}</td>
        <td>{{ data.co2_concentration }}</td>
        <td>{{ data.pm25_concentration }}</td>
        <td>{{ data.formaldehyde_concentration }}</td>
        <td>{{ data.temperature }}</td>
        <td>{{ data.humidity }}</td>
        <!-- 删除按钮 -->
        <td>
          <button @click="deleteData(data.id)">删除</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
// 导入 axios 库用于发送 HTTP 请求
import axios from 'axios';

export default {
  // 组件的数据
  data() {
    return {
      airQualityData: [], // 存储从后端获取的数据
      newData: { // 新数据的初始值
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
    // 从后端获取数据
    fetchData() {
      axios.get('http://localhost:8080/api/airquality/data')
          .then(response => {
            this.airQualityData = response.data; // 更新组件的数据
          })
          .catch(error => {
            console.error('There was an error!', error); // 错误处理
          });
    },
    // 提交新数据到后端
    createData() {
      axios.post('http://localhost:8080/api/airquality/data', this.newData)
          .then(() => {
            this.fetchData(); // 提交成功后重新获取数据
          })
          .catch(error => {
            console.error('There was an error!', error); // 错误处理
          });
    },
    // 删除指定 ID 的数据
    deleteData(id) {
      axios.delete(`http://localhost:8080/api/airquality/data/${id}`)
          .then(() => {
            this.fetchData(); // 删除成功后重新获取数据
          })
          .catch(error => {
            console.error('There was an error!', error); // 错误处理
          });
    }
  },
  // 组件挂载完成后执行
  mounted() {
    this.fetchData(); // 组件加载时获取数据
  }
};
</script>

<style scoped>
/* 样式部分仅影响当前组件 */

/* 表格样式 */
table {
  width: 100%; /* 表格宽度为 100% */
  border-collapse: collapse; /* 合并表格边框 */
}

/* 表头和表格单元格的样式 */
th, td {
  padding: 8px; /* 内边距 8px */
  border: 1px solid #ccc; /* 边框颜色 */
}

/* 表单的样式 */
form {
  margin-bottom: 20px; /* 表单底部外边距 20px */
}
</style>
