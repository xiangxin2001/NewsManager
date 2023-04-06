<template>
    <div>
       <el-form :model="dataruleForm" status-icon :rules="rules" ref="dataruleForm" label-width="100px" class="demo-dataruleForm">

            <el-form-item >
               <p>重置账户是指重置您的账户的个性化数据，不包括您的账户的注册数据，账户重置后，您的账户的个性化推荐内容及历史记录都将会清零，请谨慎思考后再选择是否重置您的账户。</p>
           </el-form-item>

           <el-form-item label="密码" prop="password">
               <el-input type="password" v-model="dataruleForm.password" autocomplete="off"></el-input>
           </el-form-item>
           
           <el-form-item>
               <el-button class="submit_button" type="primary" @click="submitForm('dataruleForm')">确认重置账户</el-button>
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
   
           return {
               error_message:"",
               dataruleForm: {
                   password:'',
               },
               rules: {
                   password:[
                   {required: true,validator: validatePassword, trigger: 'blur'}
                   ],
               },
               
           };
       },
       methods: {
           submitForm(formName) {
           this.$refs[formName].validate((valid) => {
               if (valid ) {
               this.axios.post('/userinfo/reset/', {
                               password: this.dataruleForm.password,
                           }, {
                               responseType: 'json',          
                           })
                               .then(response => {
   
                                   if (response.data.code == 0) {
                                       alert('重置账户成功，请重新登录');
                                       this.logout();
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
       margin-top: 0%;
       margin-left: 25%;
       margin-right: 35%;
   }
   /deep/.el-input__inner{
       border: 1px solid #737377;
       margin-top: 0px;
   }
   .el-button--primary{
       background-color:rgba(255, 0, 0, 0.8);
       border-color:rgba(255, 0, 0, 0.8);
       margin-left: 30%;
   }
p{
    text-align: left;
    font-size: 14px;
    display: inline-block;
    margin-block-start: 1em;
    margin-block-end: 0em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    color:red;
}
   </style>