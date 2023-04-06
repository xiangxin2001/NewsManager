<template>
    <div>
       <el-form :model="dataruleForm" status-icon :rules="rules" ref="dataruleForm" label-width="100px" class="demo-dataruleForm">
           <el-form-item label="新用户名" prop="username">
               <el-input  v-model="dataruleForm.username" autocomplete="off"></el-input>
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
               error_message:"",
               dataruleForm: {
                   
                   username:'',
               },
               rules: {
                   username:[
                   {required: true,validator: checkusername, trigger: 'blur'}
                   ],
               },
               
           };
       },
       methods: {
           submitForm(formName) {
           this.$refs[formName].validate((valid) => {
               if (valid ) {
               this.axios.post('/userinfo/username/', {
                               username: this.dataruleForm.username,
                           }, {
                               responseType: 'json',          
                           })
                               .then(response => {
   
                                   if (response.data.code == 0) {
                                        window.sessionStorage.setItem('username',response.data.username);
                                        alert('修改用户名成功');
                                        this.$router.push({
                                            path:'usercenter/userinfo_show',
                                        }); 
                            
                                   } else {
                                        this.error_message = '服务器错误';
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