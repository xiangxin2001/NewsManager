<template>
    <el-container>
        <el-header><myheader></myheader></el-header>
        <el-main>
            <div class="slide">
                <el-menu
                default-active="1"
                class="el-menu-vertical-demo"
                @select="handleSelect">
                <el-menu-item index="1">
                    <span >用户信息及浏览历史</span>
                </el-menu-item>
                <el-menu-item index="2">
                    <span >信息修改</span>
                </el-menu-item>
                </el-menu>
            </div>
            <div class="main"><router-view></router-view></div>
        </el-main>
    </el-container>
</template>
  
<script>

import MyHeader  from '@/components/MyHeader.vue';
export default {
    name:"UserCenter",
    components: {
    myheader: MyHeader,
    },
    data(){
        return{

        }
    },
    methods:{
        handleSelect(key) {
            if (key==1){
                this.$router.push({
                path:"/usercenter/userinfo_show",
                });
            }else if(key==2){
                this.$router.push({
                path:"/usercenter/userinfo_change",
                });
            }
        },
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
.slide{
    width: 14%;
    height: auto;
    display: inline-block;
   
}
.main{
    width: 86%;
    height: auto;
    display: inline-flex;
    border: 1px solid #030303;;
}
.el-menu{
    width: 100%;
    display: block;
    padding: 0px;
    border-right:none;
    background-color: rgba(255, 255, 255, 0)!important;
    span{
      display: block;
      text-align: center;
      font-size: 14px;
      width: 100%;
      
    }
    
}
.el-menu-item{
    display: block;
    width: 100%;
    background-color: transparent!important;
    :hover{
        background-color:rgba(255, 255, 255, 0.5)!important;
        border: 1px solid rgba(168, 169, 169, 0.5);
    }  
}
.el-menu-item.is-active {
    color: #0267cb;
}
</style>