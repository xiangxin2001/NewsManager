<template>
    <el-container>
    <el-aside width="200px"><logo></logo></el-aside>
    <el-container>
      <el-header>
        <myheader></myheader>
      </el-header>
        <el-main>
            <newslist></newslist>
        </el-main>
    </el-container>
  </el-container>
    
    
  </template>
  
  <script>
  import Logo from '@/components/Logo.vue'
  import MyHeader  from '@/components/MyHeader.vue';
  import NewsList from'./NewsList.vue'
  export default {
    name:"Category",
    components: {
    logo:Logo,myheader:MyHeader,newslist:NewsList,
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