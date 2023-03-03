<template>
  
  <div ><el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
  <el-form-item label="用户名" prop="username">
    <el-input v-model="ruleForm.username"></el-input>
  </el-form-item>
  <el-form-item label="密码" prop="password">
    <el-input type="password" v-model="ruleForm.password" autocomplete="off"></el-input>
  </el-form-item>
  <el-form-item label="确认密码" prop="checkPassword">
    <el-input type="password" v-model="ruleForm.checkPassword" autocomplete="off"></el-input>
  </el-form-item>
  <el-form-item label="手机号" prop="mobile">
    <el-input v-model="ruleForm.mobile"></el-input>
  </el-form-item>
  <el-form-item label="邮箱" prop="email">
    <el-input v-model="ruleForm.email"></el-input>
  </el-form-item>
  <el-form-item prop="allow">
  <el-checkbox v-model="ruleForm.allow">同意《纽斯新闻（本站）用户协议》</el-checkbox>
  </el-form-item>
  <el-form-item>
    <el-button class="submit_button" type="primary" @click="submitForm('ruleForm')">注册</el-button>
    <el-button class="reset_button" @click="resetForm('ruleForm')">重置</el-button>
  </el-form-item>
  
</el-form></div>
</template>

<script>
export default {
    name:"form_register",
    data() {
      var checkemail = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('邮箱地址不能为空'));
        }
        setTimeout(() => {
          var pattern = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
          if (!pattern.test(value)) {
            callback(new Error('请输入正确的邮箱格式'));
          } else {
            let url = '/email/' + value + '/count/';
        
            this.axios.get(url, {
                responseType: 'json',
                withCredentials:true,
            }) 
            .then(response => {
              if (response.data.count > 0) {
                callback(new Error('该邮箱已被注册'));
                  
              } else {
                callback();  
              }
            })
            .catch(error => {
              console.log(error.response);
            })
          }
        }, 50);
      };
      var validatePassword = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        }else if(value.length<6){
          callback(new Error('密码长度必须大于等于6'));
        } else {
          if (this.ruleForm.checkPassword !== '') {
            this.$refs.ruleForm.validateField('checkPassword');
          }
          callback();
        }
      };
      var validatePassword2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if(value.length<6){
          callback(new Error('密码长度必须大于等于6'));
        } else if (value !== this.ruleForm.password) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      var checkmobile = (rule,value,callback)=> {
        if (!value){
          return callback(new Error('手机号不能为空'));
        }
        setTimeout(() => {
          var pattern=/^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$/;
          if(!pattern.test(value)){
            callback(new Error('手机号码格式不正确'));
          }else{
            var url ='/mobile/' + value + '/count/';
            this.axios.get(url, {
                responseType: 'json',
            }) 
            .then(response => {
              if (response.data.count > 0) {
                callback(new Error('该手机号已被注册'));
                  
              } else {
                callback();  
              }
            })
            .catch(error => {
              console.log(error.response);
            })
          }
        }, 50);
      };
      var checkusername = (rule,value,callback)=> {
        if (!value){
          return callback(new Error('用户名不能为空'));
        }
        setTimeout(() => {
          if(value.length<1||value.length>20){
            callback(new Error);
          }else{
            var url = '/username/' + value + '/count/';
            this.axios.get(url, {
                responseType: 'json',
                withCredentials:true,
            }) 
            .then(response => {
              if (response.data.count > 0) {
                callback(new Error('该用户名已被注册'));
                  
              } else {
                callback();  
              }
            })
            .catch(error => {
              console.log(error.response);
            })
          }
        }, 50);
      }

      return {
        ruleForm: {
          password: '',
          checkPassword: '',
          email: '',
          mobile:'',
          username:'',
          allow:false
        },
        rules: {
          password: [
            { required: true,validator: validatePassword, trigger: 'blur' }
          ],
          checkPassword: [
            { required: true,validator: validatePassword2, trigger: 'blur' }
          ],
          email: [
            { required: true,validator: checkemail, trigger: 'blur' }
          ],
          mobile:[
            {required: true,validator: checkmobile, trigger: 'blur'}
          ],
          username:[
            {required: true,validator: checkusername, trigger: 'blur'}
          ],
          allow:[
            {required: true,type:'boolean'}
          ]

        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid &&this.ruleForm.allow) {
            console.log('submit!');
            this.axios.post('/register/new/', {
                    username: this.ruleForm.username,
                    password: this.ruleForm.password,
                    checkPassword: this.ruleForm.checkPassword,
                    mobile: this.ruleForm.mobile,
                    email:this.ruleForm.email,
                    allow: this.ruleForm.allow
                }, {
                    responseType: 'json',
                    withCredentials:true,
                })
                    .then(response => {
                        if (response.data.code==0) {
                           console.log('yeah')
                           alert("注册成功！")
                           this.$router.push({
                            path:'/login',
                           });
                        }
                        if (response.data.code == 400) {
                            alert(response.data.errmsg)
                        }
                    })
                    .catch(error => {
                        if (error.response.code == 400) {
                            if ('non_field_errors' in error) {
                                this.error_sms_code_message = error.response;
                            } else {
                                this.error_sms_code_message = '数据有误';
                            }
                            this.error_sms_code = true;
                        } else {
                            console.log(error);
                        }
                    })

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
</script>

<style lang="less" scoped>
div{
  display:block;
  width:450px;
  margin-left: auto;
  margin-right: auto;
  .submit_button{
    width: 150px;
  };
  .reset_button{
    width: 150px;
  }

}
</style>