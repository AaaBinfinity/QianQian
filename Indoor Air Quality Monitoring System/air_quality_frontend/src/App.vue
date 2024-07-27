<template>
  <!-- 这是 Vue 组件的模板部分 -->
  <div id="app">
    <!-- 引入并使用 AirQuality 组件 -->
    <AirQuality />
  </div>
</template>

<script>
// 从组件目录下导入 AirQuality 组件
import AirQuality from './components/AirQuality.vue';

export default {
  // 组件名称
  name: 'App',
  // 注册组件，AirQuality 组件将在模板中使用
  components: {
    AirQuality
  }
};
</script>

<style>
/* 全局样式 */

/* 定义 #app 元素的样式 */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif; /* 设置字体家族 */
  -webkit-font-smoothing: antialiased; /* 对于 Webkit 浏览器，优化字体渲染 */
  -moz-osx-font-smoothing: grayscale; /* 对于 Mozilla 浏览器，优化字体渲染 */
  text-align: center; /* 文本居中对齐 */
  color: #2c3e50; /* 设置文本颜色 */
  margin-top: 60px; /* 设置顶部外边距 */
}
</style>
