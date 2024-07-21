<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>项目名称：
      <a href="#" target="_blank" rel="noopener">基于PLC的室内空气质量智能监测与分析平台</a>.
    </p>
    <h3>前后端分离项目</h3>
    <ul>
      <li><a href="#" target="_blank" rel="noopener">Vue</a></li>
      <li><a href="#" target="_blank" rel="noopener">Spring Boot</a></li>
    </ul>
    <h3>成员：</h3>
    <ul>
      <li><a href="#" target="_blank" rel="noopener">Binfinity</a></li>
      <li><a href="#" target="_blank" rel="noopener">AaaQingQing</a></li>
      <li><a href="#" target="_blank" rel="noopener">Jing—sudo</a></li>
  
    </ul>
    <h3>愿取得好成绩
    </h3>
    
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
