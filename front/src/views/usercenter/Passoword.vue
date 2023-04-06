<template>
 <div>
    <el-form :model="dataruleForm" status-icon :rules="rules" ref="dataruleForm" label-width="100px" class="demo-dataruleForm">
        <el-form-item label="旧密码" prop="old_password">
            <el-input type="password" v-model="dataruleForm.old_password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
            <el-input type="password" v-model="dataruleForm.new_password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认新密码" prop="checkPassword">
            <el-input type="password" v-model="dataruleForm.checkPassword" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button class="submit_button" type="primary" @click="submitForm('dataruleForm')">确认修改</el-button>
            <el-button class="reset_button" @click="resetForm('dataruleForm')">重置输入</el-button>
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
        var validatePasswordnew = (rule, value, callback) => {
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
        return {
            error_message:"",
            dataruleForm: {
                new_password:'',
                old_password:'',
                checkPassword:'',
            },
            rules: {
                new_password: [
                { required: true,validator: validatePasswordnew, trigger: 'blur' }
                ],
                old_password:[
                {required: true,validator: validatePassword, trigger: 'blur'}
                ],
                checkPassword: [
                    { required: true,validator: validatePassword2, trigger: 'blur' }
                ],
            },
            
        };
    },
    methods: {
        submitForm(formName) {
        this.$refs[formName].validate((valid) => {
            if (valid ) {
            this.axios.post('/userinfo/password/', {
                            old_password: this.dataruleForm.old_password,
                            new_password: this.dataruleForm.new_password,
                            new_password2:this.checkPassword,
                        }, {
                            responseType: 'json',          
                        })
                            .then(response => {

                                if (response.data.code == 0) {
                                    alert('修改密码成功，请重新登录');
                                    this.logout();
                                } else if (response.data.code === 400) {
                                    this.error_message = response.data.errmsg;
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
            this.resetForm('dataruleForm');
        },
        logout(){
            this.axios.delete('/logout/',{
                responseType:'json',
            })
            .then(res=>{
                if(res.data.code==0){
                window.sessionStorage.removeItem('logined');
                window.sessionStorage.removeItem('username');
                this.$router.push({
                    path:'/login',
                });
                }
            })
            .catch(err=>{
                alert('服务器错误');
                console.log(err);
            })
        },
    },
}
</script>

<style lang='less' scoped>
.el-form{
    margin-top: 2%;
    margin-left: 25%;
    margin-right: 35%;
}
/deep/.el-input__inner{
    border: 1px solid #737377;
    margin-top: 5px;
}
.el-button--primary{
    background-color:rgba(0,0,255,0.5);
    border-color:rgba(0,0,255,0.5);
    margin-left: 20%;
}
.el-button:not(.el-button--primary) {
    background-color:rgba(255,255,255,0.8);
    border-color:rgba(255,255,255,0.8);
}
</style>