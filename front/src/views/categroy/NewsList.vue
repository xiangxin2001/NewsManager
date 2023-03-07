<template>
 <div>
    <el-skeleton :rows="7" animated v-show="data_loading"/>
    <div> 
    <div v-for="(val,key,i) in breadcrumb" :key="i" class="bdcb" :bread="breadcrumb">
        <span><a :href="val">{{key}}</a></span>
    </div>
    </div>
    <el-main>
        <ul v-for="(news,i) in news_list" :key="i" class="news_list">
        <li><span class="time">{{ news.time }}</span><span class="news_box"><a :href="news.url">{{ news.title }}</a></span></li>
        </ul>
        <div>
        <el-pagination
            @current-change="handleCurrentChange"
            :current-page="page"
            :page-size="pagesize"
            layout="prev, pager, next, jumper"
            :total="total"
            hide-on-single-page
            background>
        </el-pagination>
  </div>
    </el-main>
 </div>
</template>

<script>
 export default {
    name:"NewsList",
    data(){
        return{
            data_loading:true,
            news_list:[],
            pagenum:1,
            page:1,
            pagesize:15,
            total:0,
            breadcrumb:{},
        }
    },
    created(){
        if(this.$route.query.page!=undefined&&this.$route.query.pagesize!=undefined){
            this.page=Number(this.$route.query.page);
            this.pagesize=Number(this.$route.query.pagesize);
        }
        let url='/news/category/'+this.$route.params.category_id;
        this.axios.get(url,{
            params:{
                page:this.page,
                pagesize:this.pagesize,
            },
            responseType:'json',
        })
        .then(res=>{
            if(res.data.code==0){
                this.data_loading=false;
                this.news_list=res.data.news_list;
                this.total=res.data.total;
                this.breadcrumb=res.data.breadcrumb;
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
        this.pagenum=Math.ceil(this.total/this.pagesize)
    },
    methods: {
        handleCurrentChange(targetpage){
            this.page=targetpage;
            let url='/news/category/'+this.$route.params.category_id;
            this.axios.get(url,{
                params:{
                    page:this.page,
                    pagesize:this.pagesize,
                },
                responseType:'json',
            })
            .then(res=>{
                if(res.data.code==0){
                    this.data_loading=false;
                    this.news_list=res.data.news_list;
                    this.total=res.data.total;
                    this.breadcrumb=res.data.breadcrumb;
                    this.$router.push({
                    path:'/category/'+this.$route.params.category_id,
                    query:{
                        page:this.page,pagesize:this.pagesize,
                    }
                    })
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
    },
 }
</script>

<style lang='less' scoped>
*{
    font-family: "Microsoft YaHei";
    padding: 0px;
    
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
.news_list{
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
.time{
    line-height: 0px;
    text-align: left;
    font-size: 8px;
    display: inline;
}
</style>

  
