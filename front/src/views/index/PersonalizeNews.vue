<template>
    <div v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.3)" element-loading-text="正在加载中">
        <div class="column_title">
            <h1>个性化推荐</h1>
        </div>
        <div class="news_container">
            <ul  class="news-list" >
                <li  class="news-list-item">
                    <span v-for="(news,i) in personalize_news_list1" :key="i" class="left">
                        <span class="time">{{ news.time }}.</span><span class="news_box"><a :href="news.url">{{ news.title }}</a></span>
                    </span>
                    <span v-for="(news,i) in personalize_news_list2" :key="i" class="right">
                        <span class="time">{{ news.time }}.</span><span class="news_box"><a :href="news.url">{{ news.title }}</a></span>
                    </span>
                </li>
            </ul>
        </div>
    </div>
</template>
   
<script>
export default {
    data(){
        return{
            personalize_news_list1:[],
            personalize_news_list2:[],
            loading:true,
            count:0,
        }
    },
    mounted(){
        let url='/news/personalizenews/';
        this.axios.get(url,{
            responseType:'json',
        })
        .then(res=>{
            if(res.data.code==0){
                this.loading=false;
                let len=res.data.personalize_news_list.length;
                this.personalize_news_list1=res.data.personalize_news_list.slice(0,len/2);
                this.personalize_news_list2=res.data.personalize_news_list.slice(len/2);
                
            }else{
                console.log(res.data.errmsg);
            }
        })
        .catch(err=>{
            console.log(err);
        })
    },
    methods:{
        
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
.column_title{
    width: 99%;
    height: 10%;
    position: relative;
    display: inline-block;
    margin-left: 1%;
}
.news_container{
    width: 100%;
    height: 90%;
    position: relative;
    display: inline-block;
    overflow-x: hidden;
    overflow-y: auto;
    .left{
        height: 100%;
        width: 50%;
        display: inline-block;
        margin-bottom: 1%;
        text-overflow: ellipsis; white-space: nowrap; overflow: hidden;
    }
    .right{
        height: 100%;
        width: 50%;
        display: inline-block;
        margin-bottom: 1%;
        text-overflow: ellipsis; white-space: nowrap; overflow: hidden;
    }
}
.news-list{
    display:block;
    ::after{
        content:'';
        display:block;
        clear:both;
    }    
    li{
        list-style:none;
        line-height: 30px;
        font-size:18px;
        position: relative;
        padding-left: 20px;
        
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
};
.time{
    line-height: 0px;
    text-align: left;
    font-size: 8px;
    display: inline;
}
</style>