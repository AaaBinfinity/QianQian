<template>
  <div id="app">
    <AirQuality />
  </div>
</template>

<script>
import AirQuality from './components/AirQuality.vue';

export default {
  name: 'App',
  components: {
    AirQuality
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
