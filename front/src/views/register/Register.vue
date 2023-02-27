<template>
  <el-container>
  <el-aside width="200px">Aside</el-aside>
  <el-container>
    <el-header>Header</el-header>
      <el-main>
        <span class="post"></span>
        <span class="register">
          <form_register/>
        </span>
      </el-main>
    <el-footer>Footer</el-footer>
  </el-container>
</el-container>
  
  
</template>

<script>
import form_register from '@/components/Form_register.vue'


export default {
    name:"Register",
    components: {
      form_register
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