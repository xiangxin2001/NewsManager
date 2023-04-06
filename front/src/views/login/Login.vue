<template>
    <el-container>
    <el-aside width="200px"><logo></logo></el-aside>
    <el-container>
      <el-header><myheader></myheader></el-header>
        <el-main style="height: 500px;">
            <span class="post">
                <img class="image" src="../../../public/img/loginpost.gif"/>
            </span>

            <span class="login_from">
                <from_login></from_login>
            </span>
        </el-main>
    </el-container>
  </el-container>
    
    
  </template>
  
  <script>
  import Logo from '@/components/Logo.vue';
  import MyHeader  from '@/components/MyHeader.vue';
  import From_login from './From_login.vue';
  export default {
    name:"Login",
    components: {
        logo:Logo,myheader:MyHeader,from_login:From_login
    },
    
  
  }
  </script  >
  
  <style lang="less" scoped>
  *{
      margin:0;
      padding:0;
      box-sizing: border-box;
      height: 100%;
  };
  
  .post{
    display: flex;
    float:left;
    width:200px;
    height: 400px;
    
  }
  .login_from{  
  display:block;
  width:450px;
  height: auto;
  margin-left: auto;
  margin-right: auto;
  margin-top: 8%;
  margin-bottom: auto;
  }

</style>