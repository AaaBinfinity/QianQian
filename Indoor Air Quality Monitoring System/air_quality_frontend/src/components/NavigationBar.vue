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
}
.nav-bar button {
  margin-right: 10px;
  padding: 10px 20px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.nav-bar button:hover {
  background-color: #1a252f;
}
</style>
