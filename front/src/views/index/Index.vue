<template>
    <el-container>
    <el-aside width="200px"><logo></logo></el-aside>
    <el-container>
      <el-header><myheader></myheader></el-header>
        <el-main>
        </el-main>
      <el-footer>Footer</el-footer>
    </el-container>
  </el-container>
    
    
  </template>
  
  <script>
  import Logo from '@/components/Logo.vue'
  import MyHeader  from '@/components/MyHeader.vue';
  export default {
    name:"Index",
    components: {
      logo:Logo,myheader:MyHeader
    }
  
  }
  </script  >
  
  <style lang="less" scoped>
  *{
      margin:0;
      padding:0;
      box-sizing: border-box;
      height: 100%;
  };
  </style>