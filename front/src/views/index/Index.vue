<template>
    <el-container>
    <el-aside width="200px"><logo></logo></el-aside>
    <el-container>
      <el-header><myheader></myheader></el-header>
        <el-main>
          <div class="login_not_required">
            <div class="latest_news">
              <LatestNews></LatestNews>
            </div>
            <div class="hot_news"> 
              <HotNews></HotNews>
            </div>
          </div>
          <div class="login_required">
            <PersonalizeNews v-if="logined=='true'"></PersonalizeNews>
          </div>
        </el-main>
    </el-container>
  </el-container>
    
    
  </template>
  
  <script>
  import Logo from '@/components/Logo.vue';
  import MyHeader  from '@/components/MyHeader.vue';
  import HotNews from'@/views/index/HotNews.vue';
  import LatestNews from '@/views/index/LatestNews.vue';
  import PersonalizeNews from '@/views/index/PersonalizeNews.vue';
  export default {
    name:"Index",
    components: {
      logo:Logo,myheader:MyHeader,HotNews,LatestNews,PersonalizeNews,
    },
    data(){
      return{
        logined:window.sessionStorage.getItem('logined'),
      }
    },
    mounted(){
      this.logined=window.sessionStorage.getItem('logined');
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
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-thumb {
    background: #ffffff; // 滑块颜色
    border-radius: 5px; // 滑块圆角
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(245, 44, 242, 0.519);
}
::-webkit-scrollbar-track {
    border-radius: 5px; // 轨道圆角
    background-color: rgba(255,255,255,0.5) // 轨道颜色 
}

.login_not_required{
  height: 320px;
  display: block;
  position: relative;
  .latest_news{
    height: 100%;
    width: 69%;
    display: inline-block;
    position: relative;
    background-color: rgba(255,255,255,0.5);
   
  }
  .hot_news{
    height:100%;
    width: 30%;
    margin-left: 1%;
    display: inline-block;
    position: relative;
    background-color: rgba(255,255,255,0.5);
  }
  margin-bottom: 1%;
}
.login_required{
  height: 600px;
  display: flex;
  position: relative;
  overflow-x: hidden;
  overflow-y: auto;
  background-color: rgba(255,255,255,0.5);
}
  </style>