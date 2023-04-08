<template>
    <div v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.3)" element-loading-text="正在加载中">
        <ul  class="infinite-list" v-infinite-scroll="load" style="overflow:auto">
            <li v-for="(news,i) in personalize_news" :key="i" class="infinite-list-item">
                <span class="time">{{ news.time }}</span><span class="news_box"><a :href="news.url">{{ news.title }}</a></span>
            </li>
        </ul>
    </div>
</template>
   
<script>
export default {
    data(){
        return{
            personalize_news:[],
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
                this.personalize_news-res.data.personalize_news;
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
            let url='/news/personalizenews';
            this.axios.get(url,{
                responseType:'json',
            })
            .then(res=>{
                if(res.data.code==0){
                    this.loading=false;
                    this.personalize_news-res.data.personalize_news;
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
div{
    width: 100%;
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
        font-size:22px;
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