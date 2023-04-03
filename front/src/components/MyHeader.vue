<template>
 <div>
   <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <div class="first">
      <el-menu-item index="1"><a href="/" target="_self"><div>网站首页</div></a></el-menu-item>
      </div>
      <div class="second">
         <el-submenu index="2">
            <template slot="title"><a href="#"><div>新闻分类</div></a></template>
            <el-menu-item index="2-1"><a href="/category/1" target="_self"><div>政治新闻</div></a></el-menu-item>
            <el-menu-item index="2-2"><a href="/category/2" target="_self"><div>财经新闻</div></a></el-menu-item>
            <el-menu-item index="2-3"><a href="/category/3" target="_self"><div>社会新闻</div></a></el-menu-item>
            <el-menu-item index="2-4"><a href="/category/4" target="_self"><div>文化娱乐</div></a></el-menu-item>
            <el-menu-item index="2-5"><a href="/category/5" target="_self"><div>体育新闻</div></a></el-menu-item>
            <el-menu-item index="2-6"><a href="/category/6" target="_self"><div>健康新闻</div></a></el-menu-item>
            <el-menu-item index="2-7"><a href="/category/7" target="_self"><div>军事新闻</div></a></el-menu-item>
            <el-menu-item index="2-8"><a href="/category/8" target="_self"><div>国际新闻</div></a></el-menu-item>
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
                     v-model="search_data"
                     @keyup.enter.native="search_news">
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
      <div class="right_header" v-show="logined" style="width: auto;">
      <el-submenu index="4">
         <template slot="title"><div><i class="el-icon-user-solid" style="display: inline-block;"></i><span style="display: inline-block;">{{ username }}</span></div></template>
            <el-menu-item index="4-1"><a href="/usercenter" target="_self"><div>用户中心</div></a></el-menu-item>
            <el-menu-item index="4-2"><a href="#" target="_self" @click='logout'><div>退出登录</div></a></el-menu-item>
      </el-submenu>
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
        reg_and_login:false,
        logined:false,
        username:"",
      };
    },
    
    methods: {
      
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      logout(){
         this.axios.delete('/logout/',{
            responseType:'json',
         })
         .then(res=>{
            if(res.data.code==0){
               console.log("55")
               window.sessionStorage.removeItem('logined');
               window.sessionStorage.removeItem('username');
               this.username="";
               this.logined=false;
               this.reg_and_login=true;
            }
         })
         .catch(err=>{
            alert('服务器错误');
            console.log(err);
         })
      },
      search_news(){
         
         if(this.logined){
            if(this.search_data.length>=1){
               
               window.sessionStorage.setItem('q',this.search_data)
               this.$router.push({
                  path:'/search',
                  query:{
                     q:this.search_data,
                  }
               });
               location.reload();
            }else{
               alert('暂不支持无关键字搜索，请输入关键字')
            }

         }else{
            alert('登录后方可搜索')
         }
      }
    },
    created(){
      var pathname=window.location.pathname;
      // console.log(pathname);
      if(!window.sessionStorage.getItem('logined')){

         this.axios.get('/login/userlogin/',{
         },{
            responseType: 'json',
         })
         .then(res=>{
            this.logined=res.data.logined;
            if(this.logined){
               this.username=res.data.username;
               window.sessionStorage.setItem('username',res.data.username);
               window.sessionStorage.setItem('logined',true);
               if(pathname=="/reg"||pathname=='/login'){
                  this.$router.push({
                     path:"/",
                  });
               }
               this.reg_and_login=false;

            }
         })
         .catch(err=>{
            console.log(err);
         })
         
         
      }else{
         this.logined=true;
         this.username=window.sessionStorage.getItem('username');
         if(pathname=="/reg"||pathname=='/login'){
            this.$router.push({
               path:"/",
            });
         }
      }
      if(!this.logined){
         if (pathname=="/reg"||pathname=="/reg#"){
            this.reg=true;
         }
         else if(pathname=='/login'||pathname=="/login#"){
            this.login=true;
         }
         else{
            this.reg_and_login=true;
            if(pathname=='/search'){
               alert("登录后可使用搜索功能")
               this.$router.push({
                  path:"/login"
               })
            }
         }
      }
   },
 }
</script>

<style lang='less' scoped>
   a{ text-decoration:none;    
      div{
         color: rgb(0, 0, 0);    
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