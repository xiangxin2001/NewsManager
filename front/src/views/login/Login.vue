<template>
    <el-container>
    <el-aside width="200px"><logo></logo></el-aside>
    <el-container>
      <el-header><myheader></myheader></el-header>
        <el-main style="height: 400px;">
            <div class="login_form"><el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="ruleForm.username"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" v-model="ruleForm.password" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button class="submit_button" type="primary" @click="submitForm('ruleForm')">登录</el-button>
                    <el-button class="reset_button" @click="resetForm('ruleForm')">重置</el-button>
                </el-form-item>
  
                </el-form>
            </div>
        </el-main>
    </el-container>
  </el-container>
    
    
  </template>
  
  <script>
  import Logo from '@/components/Logo.vue'
  import MyHeader  from '@/components/MyHeader.vue';
  export default {
    name:"Login",
    components: {
        logo:Logo,myheader:MyHeader
    },
    data() {

      var validatePassword = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        }else if(value.length<6){
          callback(new Error('密码长度必须大于等于6'));
        } else {
          callback();
        }
      };
      var checkusername = (rule,value,callback)=> {
        if (!value){
          return callback(new Error('此项不能为空'));
        }
        else{
            callback()
        }
      }

      return {
        ruleForm: {
          password: '',
          username:'',
        },
        rules: {
          password: [
            { required: true,validator: validatePassword, trigger: 'blur' }
          ],
          username:[
            {required: true,validator: checkusername, trigger: 'blur'}
          ]
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid &&this.ruleForm.allow) {
            console.log('submit!');

          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
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
  .login_form{
  display:block;
  width:450px;
  height: 40px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 8%;
  margin-bottom: auto;
  }
  .submit_button{
    width: 150px;
  };
  .reset_button{
    width: 150px;
  }
  </style>