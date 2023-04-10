<template>
    <div v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.3)" element-loading-text="正在加载中">
        <div class="column_title">
            <h1>热点新闻</h1>
        </div>
        <div class="hotnew_container">
            <ul v-for="(news,i) in hot_news" :key="i" class="news_list">
            <li><label>{{ i+1 }}.</label><span class="news_box"><a :href="news.url">{{ news.title }}</a></span></li>
        </ul>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return{
            hot_news:[],
            loading:true,
        }
    },
    mounted(){
        let url='/news/hotnews/';
        this.axios.get(url,{
            responseType:'json',
        })
        .then(res=>{
            if(res.data.code==0){
                this.loading=false;
                this.hot_news=res.data.hot_news;
                
            }else{
                console.log(res.data.errmsg);
            }
        })
        .catch(err=>{
            console.log(err);
        })
    }
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
.column_title{
    width: 95%;
    height: 15%;
    position:relative;
    display: inline-block;
    margin-left: 5%;
}
.hotnew_container{
    width: 100%;
    height: 85%;
    position:relative;
    display: inline-block;
    overflow-y: auto;
    overflow-x: hidden;
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
        line-height: 20px;
        font-size:16px;
        position: relative;
        padding-left: 0;
        text-overflow: ellipsis; white-space: nowrap; overflow: hidden;

        label{
            display: inline-block;
            font-weight: 600;
            margin-right: 5px;
        }

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
</style>