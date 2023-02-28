<template>
 <div>
   <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <div class="first">
      <el-menu-item index="1"><a href="/" target="_self"><div>网站首页</div></a></el-menu-item>
      </div>
      <div class="second">
         <el-submenu index="2">
            <template slot="title"><a href="#"><div>新闻分类</div></a></template>
            <el-menu-item index="2-1"><a href="#" target="_self"><div>政治新闻</div></a></el-menu-item>
            <el-menu-item index="2-2"><a href="#" target="_self"><div>财经新闻</div></a></el-menu-item>
            <el-menu-item index="2-3"><a href="#" target="_self"><div>社会新闻</div></a></el-menu-item>
            <el-menu-item index="2-4"><a href="#" target="_self"><div>文化娱乐</div></a></el-menu-item>
            <el-menu-item index="2-5"><a href="#" target="_self"><div>体育新闻</div></a></el-menu-item>
            <el-menu-item index="2-6"><a href="#" target="_self"><div>健康新闻</div></a></el-menu-item>
            <el-menu-item index="2-7"><a href="#" target="_self"><div>军事新闻</div></a></el-menu-item>
            <el-menu-item index="2-8"><a href="#" target="_self"><div>国际新闻</div></a></el-menu-item>
            <!-- <el-submenu index="2-4">
               <template slot="title">选项4</template>
               <el-menu-item index="2-4-1">选项1</el-menu-item>
               <el-menu-item index="2-4-2">选项2</el-menu-item>
               <el-menu-item index="2-4-3">选项3</el-menu-item>
            </el-submenu> -->
         </el-submenu>
      </div>
      <div class="search_bar">
         <el-menu-item index="3" >
               <div class="grid-content bg-purple">
                  <el-input
                     placeholder="请输入内容"
                     prefix-icon="el-icon-search"
                     v-model="search_data">
                  </el-input>
               </div>
         </el-menu-item>
      </div>
      <div class="right_header" v-show="reg">
      <el-menu-item index="4" ><a href="/login" target="_self"><div>登录</div></a></el-menu-item>
      </div>
      <div class="right_header" v-show="login">
      <el-menu-item index="4" ><a href="/reg" target="_self"><div>注册</div></a></el-menu-item>
      </div>
      <div class="right_header" v-show="reg_and_login">
      <el-menu-item index="4" ><a href="/reg" target="_self"><div>注册</div></a></el-menu-item>
      <el-menu-item index="5" ><a href="/login" target="_self"><div>登录</div></a></el-menu-item>
      </div>
   </el-menu>
<div class="line"></div>

 </div>
</template>

<script>
 export default {
    name:"MyHeader",
    data() {
      return {
        activeIndex: '0',
        activeIndex2: '0',
        search_data:"",
        reg:false,
        login:false,
        reg_and_login:false
      };
    },
    
    methods: {
      
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
    },
    created(){
      var pathname=window.location.pathname;
      console.log(pathname);
      if (pathname=="/reg"||pathname=="/reg#"){
         this.reg=true;
      }
      else if(pathname=='/login'||pathname=="/login#"){
         this.login=true;
      }
      else{
         this.reg_and_login=true;
      }
   },
 }
</script>

<style lang='less' scoped>
   a{ text-decoration:none;
      
      :hover{
         color: black;
         display: inline-flex;
      }
      
      div{
         color: rgba(105, 105, 121, 0.503);
         
      }
   }
   .first{
      display: inline-flex;

   }
   .second{
      display: inline-flex;
   }
   .search_bar{
      display: inline-flex;
      left:50% ;
      
   }
   .right_header{
      display: flex;
      margin-right: 0px;
      float:right;
   }
</style>