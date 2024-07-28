<template>
  <div class="nav-bar">
    <button @click="navigate('1m')">近1分钟</button>
    <button @click="navigate('1h')">近1小时</button>
    <button @click="navigate('1d')">近1天</button>
    <button @click="navigate('1w')">近1周</button>
    <button @click="navigate('1M')">近1个月</button>
    <button @click="navigate('6M')">近半年</button>
    <button @click="navigate('1y')">近1年</button>
    <button @click="navigate('all')">ALL</button>
    <button @click="navigate('data')">数据管理</button>
  </div>
</template>

<script>
export default {
  name: 'NavigationBar',
  methods: {
    navigate(range) {
      this.$router.push({ path: `/${range}` });
    }
  }
};
</script>

<style scoped>
.nav-bar {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  background-color: #e0f7fa;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}
.nav-bar button {
  margin: 0 10px;
  padding: 10px 20px;
  background-color: #5aa9d5;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease, transform 0.2s ease;
}
.nav-bar button:hover {
  background-color: #0288d1;
  transform: scale(1.1);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}
.nav-bar button:active {
  transform: scale(0.9);
}
</style>
