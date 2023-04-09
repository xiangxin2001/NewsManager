<template>
 <div class="login_form" >
    <el-form :model="loginruleForm" status-icon :rules="rules" ref="loginruleForm" label-width="100px" class="demo-loginruleForm">
                <el-form-item >
                    <div class="login_pic"></div>
                </el-form-item>
                <el-form-item label="用户名" prop="username" @keyup.enter.native="submitForm('loginruleForm')">
                    <el-input v-model="loginruleForm.username"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password" @keyup.enter.native="submitForm('loginruleForm')">
                    <el-input type="password" v-model="loginruleForm.password" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item prop="remember" @keyup.enter.native="submitForm('loginruleForm')">
                    <el-checkbox v-model="loginruleForm.remember">保持登录</el-checkbox>
                </el-form-item>
                <el-form-item>
                    <el-button class="submit_button" type="primary" @click="submitForm('loginruleForm')">登录</el-button>
                    <el-button class="reset_button" @click="resetForm('loginruleForm')">重置</el-button>
                </el-form-item>
                
                
    </el-form>
 </div>
</template>

<script>
 export default {

data() {

var validatePassword = (rule, value, callback) => {
  if (value === '') {
    return callback(new Error('请输入密码'));
  }else if(value.length<6){
    return callback(new Error('密码长度必须大于等于6'));
  } else {
    return callback();
  }
};
var checkusername = (rule,value,callback)=> {
  if (!value){
    return callback(new Error('此项不能为空'));
  }
  else{
    return callback()
  }
};

return {
  error_message:"",
  loginruleForm: {
    password: '',
    username:'',
    remember:false,
  },
  rules: {
    password: [
      { required: true,validator: validatePassword, trigger: 'blur' }
    ],
    username:[
      {required: true,validator: checkusername, trigger: 'blur'}
    ],
    remember:[{required:true,type:"boolean"}]
  }
};
},
methods: {

submitForm(formName) {
  this.$refs[formName].validate((valid) => {
    if (valid ) {
      this.axios.post('/login/userlogin/', {
                    username: this.loginruleForm.username,
                    password: this.loginruleForm.password,
                    remember:this.loginruleForm.remember,
                }, {
                    responseType: 'json',
                    // 发送请求的时候, 携带上cookie
                    
                })
                    .then(response => {

                        if (response.data.code == 0) {
                            // 跳转页面
                            window.sessionStorage.setItem('username',response.data.username);
                            this.$router.push({
                              path:'/',
                            });
                        } else if (response.data.code === 400) {
                            this.error_message = '用户名或密码错误';
                            this.alert_error();
                            
                        }
                    })
                    .catch(error => {
                            console.log(error)
                            this.error_message = '服务器错误';
                            this.alert_error();
                        
                    })
            
    } else {
      console.log('error submit!!');
      return false;
    }
  });
},
resetForm(formName) {
  this.$refs[formName].resetFields();
},
alert_error(){
        alert(this.error_message);
        this.error_message="";
        this.resetForm('loginruleForm');
}
}
}
</script>

<style lang='less' scoped>
div{
  display:inline-block;
  width:450px;
  height: auto;
  margin-left: auto;
  margin-right: auto;
  .submit_button{
    width: 150px;
  };
  .reset_button{
    width: 150px;
  }
  
}
 .login_pic{
    display: block;
    height: 40px;
    width: 400px;
    background-image: url('../../../public/img/loginpic.png');
    background-repeat: no-repeat;
  }

/deep/.el-input__inner{
    border: 2px solid #737377;
    margin-top: 5px;
}
/deep/.el-input .el-input__inner::placeholder {
    color:rgba(0,0,0, 0.7);
}
.el-button--primary{
    background-color:rgba(0,0,255,0.5);
    border-color:rgba(0,0,255,0.5);
}
.el-button:not(.el-button--primary) {
    background-color:rgba(255,255,255,0.8);
    border-color:rgba(255,255,255,0.8);
}
</style>