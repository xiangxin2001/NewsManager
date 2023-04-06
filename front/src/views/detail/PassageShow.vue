<template>
<div>
<el-skeleton :rows="7" animated v-show="data_not_loaded"/>
<el-item> 
    <div v-for="(val,key,i) in breadcrumb" :key="i" class="bdcb" :bread="breadcrumb">
        <span><a :href="val">{{key}}</a></span>
    </div>
</el-item>
<el-main>
 <h1 class="title">{{news.title}}</h1>
 <div v-html="news.passage" class="passageshow"></div>
 <div class="passagefoot">
    <p>来源：{{news.news_from}}</p>
    <p>浏览量：{{ news.visited }}</p>
    <div><a :href="news.url" target="_blank">查看源网页</a></div>
 </div>
 
</el-main>
</div>
</template>

<script>
 export default {
    name:"PassageShow",
    data(){
        return{
            news_id:this.$route.params.news_id,
            news:{
                title:"",
                category:"",
                passage:"",
                news_from:"",
                url:"",
                visited:"",
            },
            breadcrumb:{},
            data_not_loaded:true,
        }
    },
    methods:{

    },
    created(){
        let url='/news/'+this.news_id;
        this.axios.get(url,{
            responseType:'json',
        })
        .then(res=>{
            if(res.data.code==0){
                this.data_not_loaded=false;
                this.news.title=res.data.news.title;
                this.news.category=res.data.news.category;
                this.news.passage=res.data.news.passage;
                this.news.news_from=res.data.news.news_from;
                this.news.url=res.data.news.url;
                this.breadcrumb=res.data.news.breadcrumb;
                this.news.visited=res.data.news.visited;
            }else{
                console.log(res.data.errmsg);
                this.$router.push({
                    path:'/404'
                })
            }
        })
        .catch(err=>{
            this.$router.push({
                path:'/404'
            })
            console.log(err);
        })
    }
 }
</script>

<style lang='less' scoped>
*{
    font-family: "Microsoft YaHei";
    
};
.bdcb{
    background-color: rgba(255, 255, 255, 0.5);
    border: 1px solid #030303;
    display: inline-flex;
    
    border-radius: 6px;
    a{  line-height:25px;
        margin-left: 10px;
        margin-right: 10px;
        text-align: center;
        font-size: 18px;
        text-decoration: none;
        color:black
    };
    :hover{
        background-color: rgba(57, 222, 156, 0.5);
    };
};
.title{
    font-size: 40px; 
    line-height: 50px;
    padding-top: 35px;
    padding-bottom: 24px;
    font-weight: 600;
    text-align: center;
    display: block;
};
.passageshow{
    text-align: left;
    font-size: 18px;
    display: inline-block;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
};
img{
    overflow-clip-margin: content-box;
    overflow: clip;
    border: none;
};
.passagefoot{
    display: inline-block;
    margin-top:30px;
    font-size: 18px;
    a{
        text-decoration:none;
        color: #000000;
        font-size: 18px;
    };
    div{
        text-align: center;
        :hover{
        display:inline-block;
        height: 40px;
        width: 150px;
        background-color: rgba(255, 255, 255, 0.2);
        border:1px solid;
        border-color: #40f2f5;
        border-radius:6px;
        }
    }
    
    
};

</style>