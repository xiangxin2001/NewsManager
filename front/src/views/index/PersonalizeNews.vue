<template>
    <div v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.3)" element-loading-text="正在加载中">
        <div class="column_title">
            <h1>个性化推荐</h1>
        </div>
        <div class="news_container">
            <ul  class="infinite-list" v-infinite-scroll="load" style="overflow:auto">
                <li v-for="(news,i) in personalize_news_list" :key="i" class="infinite-list-item">
                    <span class="time">{{ news.time }}.</span><span class="news_box"><a :href="news.url">{{ news.title }}</a></span>
                    <!-- <span class="time">{{ news.time }}.</span><span class="news_box"><a :href="news.url">{{ news.title }}</a></span> -->
                </li>
            </ul>
        </div>
    </div>
</template>
   
<script>
export default {
    data(){
        return{
            personalize_news_list:[],
            loading:true,
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
                this.personalize_news_list=res.data.personalize_news_list;
            }else{
                console.log(res.data.errmsg);
            }
        })
        .catch(err=>{
            console.log(err);
        })
    },
    methods:{
        load(){
            this.loading=true;
            let url='/news/personalizenews/';
            this.axios.get(url,{
                responseType:'json',
            })
            .then(res=>{
                if(res.data.code==0){
                    this.loading=false;
                    this.personalize_news_list-res.data.personalize_news_list;
                }else{
                    console.log(res.data.errmsg);
                }
            })
            .catch(err=>{
                console.log(err);
            })
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
}
.infinite-list{
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
            position: absolute;
            top: 50%;
            left: 0;
            margin-top: -6px;
            width: 15px;
            height: 15px;
            border-radius:25%;
            background: rgba(245, 44, 242, 0.519)
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
</style>