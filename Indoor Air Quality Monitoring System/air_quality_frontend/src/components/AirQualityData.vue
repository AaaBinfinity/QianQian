<template>
  <h1>室内空气质量监测</h1>
  <NavigationBar :currentView="'all'" @navigate="handleNavigate" />
  <div class="container">
    <form @submit.prevent="createData" class="data-form">
      <div class="form-row">
        <div class="form-group">
          <label>时间:</label>
          <input v-model="newData.timestamp" type="datetime-local" required />
        </div>
        <div class="form-group">
          <label>二氧化碳浓度:</label>
          <input v-model="newData.co2_concentration" type="number" step="0.01" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>PM2.5浓度:</label>
          <input v-model="newData.pm25_concentration" type="number" step="0.01" required />
        </div>
        <div class="form-group">
          <label>甲醛浓度:</label>
          <input v-model="newData.formaldehyde_concentration" type="number" step="0.01" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>温度:</label>
          <input v-model="newData.temperature" type="number" step="0.01" required />
        </div>
        <div class="form-group">
          <label>湿度:</label>
          <input v-model="newData.humidity" type="number" step="0.01" required />
        </div>
      </div>
      <button type="submit" class="submit-button">添加数据</button>
    </form>

    <div class="filter-form">
      <h2>筛选数据</h2>
      <div class="form-row">
        <div class="form-group">
          <label>开始时间:</label>
          <input v-model="filter.startTime" type="datetime-local" />
        </div>
        <div class="form-group">
          <label>结束时间:</label>
          <input v-model="filter.endTime" type="datetime-local" />
        </div>
      </div>
    </div>

    <table>
      <thead>
      <tr>
        <th>时间</th>
        <th>二氧化碳浓度 ppm</th>
        <th>PM2.5浓度 µg/m³</th>
        <th>甲醛浓度 mg/m³</th>
        <th>温度 °C</th>
        <th>湿度 % (相对湿度)</th>
        <th>操作</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="data in paginatedAirQualityData" :key="data.id">
        <td>{{ data.timestamp }}</td>
        <td>{{ data.co2_concentration }}</td>
        <td>{{ data.pm25_concentration }}</td>
        <td>{{ data.formaldehyde_concentration }}</td>
        <td>{{ data.temperature }}</td>
        <td>{{ data.humidity }}</td>
        <td>
          <button @click="confirmDelete(data.id)" class="delete-button">删除</button>
        </td>
      </tr>
      </tbody>
    </table>

    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
    </div>

    <div class="button-group">
      <button @click="saveDataToFile" class="action-button">保存数据到文件</button>
      <button @click="printData" class="action-button">打印数据</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { saveAs } from 'file-saver';
import NavigationBar from "@/components/NavigationBar.vue";

export default {
  components: { NavigationBar },
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
      },
      filter: {
        startTime: '',
        endTime: ''
      },
      currentPage: 1,
      itemsPerPage: 20
    };
  },
  computed: {
    filteredAirQualityData() {
      const { startTime, endTime } = this.filter;
      if (startTime && endTime) {
        return this.airQualityData.filter(data => {
          const timestamp = new Date(data.timestamp).getTime();
          return timestamp >= new Date(startTime).getTime() && timestamp <= new Date(endTime).getTime();
        });
      }
      return this.airQualityData;
    },
    paginatedAirQualityData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = this.currentPage * this.itemsPerPage;
      return this.filteredAirQualityData.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredAirQualityData.length / this.itemsPerPage);
    }
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
            alert('数据添加成功！');
            this.fetchData();
          })
          .catch(error => {
            console.error('There was an error!', error);
          });
    },
    confirmDelete(id) {
      if (confirm('确定要删除这条数据吗？')) {
        this.deleteData(id);
      }
    },
    deleteData(id) {
      axios.delete(`http://localhost:8080/api/airquality/data/${id}`)
          .then(() => {
            alert('数据删除成功！');
            this.fetchData();
          })
          .catch(error => {
            console.error('There was an error!', error);
          });
    },
    saveDataToFile() {
      const dataStr = JSON.stringify(this.airQualityData, null, 2);
      const blob = new Blob([dataStr], { type: 'application/json' });
      saveAs(blob, 'air_quality_data.json');
    },
    printData() {
      const printContent = document.createElement('div');
      const tableHtml = `
        <table>
          <thead>
            <tr>
              <th>时间</th>
              <th>二氧化碳浓度 ppm</th>
              <th>PM2.5浓度 µg/m³</th>
              <th>甲醛浓度 mg/m³</th>
              <th>温度 °C</th>
              <th>湿度 %</th>
            </tr>
          </thead>
          <tbody>
            ${this.filteredAirQualityData.map(data => `
              <tr>
                <td>${data.timestamp}</td>
                <td>${data.co2_concentration}</td>
                <td>${data.pm25_concentration}</td>
                <td>${data.formaldehyde_concentration}</td>
                <td>${data.temperature}</td>
                <td>${data.humidity}</td>
              </tr>`).join('')}
          </tbody>
        </table>`;
      printContent.innerHTML = tableHtml;
      const printWindow = window.open('', '', 'width=800,height=600');
      printWindow.document.write(printContent.innerHTML);
      printWindow.document.close();
      printWindow.print();
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    }
  },
  mounted() {
    this.fetchData();
    setInterval(this.fetchData, 1000);
  }
};
</script>

<style scoped>
.container {
  font-family: Arial, sans-serif;
  background-color: #f0f8ff;
  padding: 20px;
  border-radius: 8px;
  max-width: 80%;
  margin: 0 auto;
}

h1 {
  color: #4682b4;
  text-align: center;
  margin-bottom: 20px;
}

.data-form, .filter-form {
  background-color: #e6f7ff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.filter-form {
  margin-top: 20px;
}

h2 {
  color: #4682b4;
  text-align: center;
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.form-group {
  flex: 1;
  margin-right: 10px;
}

.form-group:last-child {
  margin-right: 0;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

input[type="datetime-local"],
input[type="number"] {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-button {
  background-color: #5bc0de;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #31b0d5;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th, td {
  padding: 12px;
  border: 1px solid #ccc;
  text-align: left;
}

th {
  background-color: #d1ecf1;
  color: #007bff;
}

tbody tr:nth-child(odd) {
  background-color: #f9f9f9;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete-button:hover {
  background-color: #e4293b;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.action-button {
  background-color: #5bc0de;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #31b0d5;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.pagination button {
  background-color: #5bc0de;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pagination button:hover {
  background-color: #31b0d5;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination span {
  margin: 0 10px;
}
</style>
