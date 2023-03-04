<template>
  <el-container>
  <el-aside width="200px"><logo></logo></el-aside>
  <el-container>
    <el-header><myheader></myheader></el-header>
      <el-main>
        <span class="post"></span>
        <span class="register">
          <form_register/>
        </span>
      </el-main>
  </el-container>
</el-container>
  
  
</template>

<script>

import form_register from '@/views/register/Form_register.vue'
import Logo from '@/components/Logo.vue'
import MyHeader  from '@/components/MyHeader.vue';
export default {
  name:"Register",
  components: {
    form_register:form_register,logo:Logo,myheader:MyHeader
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
.post{
  float: left;
  background-image: url("../../../public/img/ai12.png");
  width: 400px;
  height: 450px;
  display: inline-flex;
 
};
.register{

    font-weight: 600;
    margin-inline: 3;
    display: inline-flex;
    
}
</style>