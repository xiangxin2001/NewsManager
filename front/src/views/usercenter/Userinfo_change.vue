!<template>
 <div>
    <el-form :model="loginruleForm" status-icon :rules="rules" ref="loginruleForm" label-width="100px" class="demo-loginruleForm">
                <el-form-item >
                    <div class="login_pic"></div>
                </el-form-item>
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="loginruleForm.username"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" v-model="loginruleForm.password" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item prop="remember">
                    <el-checkbox v-model="loginruleForm.remember">保持登录</el-checkbox>
                </el-form-item>
                <!-- <el-form-item>
                    <el-button class="submit_button" type="primary" @click="submitForm('loginruleForm')">登录</el-button>
                    <el-button class="reset_button" @click="resetForm('loginruleForm')">重置</el-button>
                </el-form-item> -->
                
                
    </el-form>
 </div>
</template>

<script>
 export default {
 }
</script>

<style lang='less' scoped>
 
</style>