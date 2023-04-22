<template>
 <div v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.3)" element-loading-text="正在加载中">
    <div class="category">
        <span class="column_title">
            <h1>最新消息</h1>
        </span>
        <span class="category_menu">
            <el-menu
                v-for="(catname,id) in category" :key="id"
                mode="horizontal"
                :default-active=default_active
                class="el-menu-demo"
                @select="load_news">
                <el-menu-item :index="id">
                    <span >{{catname}}</span>
                </el-menu-item>
            </el-menu>
        </span>
    </div>
    
    <div class="news_container">
        <div class="left">
        <ul v-for="(news,i) in news_list1" :key="i" class="news_list">
            <li><span class="news_box"><a :href="news.url">{{ news.title }}</a></span></li>
        </ul>
        </div>
        <div class="right">
            <ul v-for="(news,i) in news_list2" :key="i" class="news_list">
                <li><span class="news_box"><a :href="news.url">{{ news.title }}</a></span></li>
            </ul>
        </div>
    </div>
 </div>
</template>

<script>
 export default {
    data(){
        return{
            latest_news:{},
            news_list1:[],
            news_list2:[],
            loading:true,
            category:{},
            default_active:1,
        }
    },
    mounted(){
        let url='/news/latestnews/';
        this.axios.get(url,{
            responseType:'json',
        })
        .then(res=>{
            if(res.data.code==0){
                this.loading=false;
                this.latest_news=res.data.latest_news;
                this.category=res.data.category;
                this.news_list1=this.latest_news[1].slice(0,5);
                this.news_list2=this.latest_news[1].slice(5);
            }else{
                console.log(res.data.errmsg);
            }
        })
        .catch(err=>{
            console.log(err);
        })
    },
    methods:{
        load_news(key){
            if(!this.loading){
                this.default_active=key;
                this.news_list1=this.latest_news[key].slice(0,5);
                this.news_list2=this.latest_news[key].slice(5);
            }
        }
    },
 }
</script>

<style lang='less' scoped>
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
.category{
    position:relative;
    width: 100%;
    height: 20%;
    display: inline-block;
    .column_title{
        width: 18%;
        height: 100%;
        text-align: center center;
        
        position:absolute;
        display: inline-block;
        margin-left: 2%;
    }
    .category_menu{
        margin-left: 12%;
        width: 80%;
        height: 100%;
        position: relative;
        display: inline-block;
    }
}


.news_container{
    width: 100%;
    height: 79%;
    position: relative;
    display: inline-block;

    overflow-y: auto;
    .left{
        height: 100%;
        width: 50%;
        display: inline-block;
    }
    .right{
        height: 100%;
        width: 50%;
        display: inline-block;
    }
} 
.news_list{
    display:block;
    ::after{
        content:'';
        display:block;
        clear:both;
    } 
    li{
        list-style:none;
        line-height: 25px;
        font-size:16px;
        position: relative;
        padding-left: 0;
        text-overflow: ellipsis; white-space: nowrap; overflow: hidden;

        ::before {
            content: "";
        };
        .news_box:hover{
            padding-inline: 5px;
            background-color: rgba(57, 222, 156, 0.5);
            border: 1px solid rgba(0, 255, 255, 0.5);
        };
        a{
            line-height: 0px;
            text-decoration: none;
            color: #030303;
        }
    }
}
  
/deep/.el-menu::after, .el-menu::before {
    position: absolute;
    display: inline;
    content: "";
}
/deep/.el-menu.el-menu--horizontal{
    border: 0px;
}
/deep/.el-menu--horizontal>.el-menu-item{
    font-size: medium;
    font-weight: 600;
}
</style>