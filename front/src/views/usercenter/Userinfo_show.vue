<template>
 <div>
    <div class="userinfo" v-loading="loading" element-loading-background="rgba(255, 255, 255,0)" element-loading-text="正在加载中">
        <h3>用户信息</h3>
        <ul>
            <label>用户名：</label><li>{{userinfo.username}}</li><br/>
            <label>手机号：</label><li>{{ userinfo.mobile }}</li><br/>
            <label>邮箱：</label><li>{{ userinfo.email }}</li><br/>
            <label>uid:</label><li>{{ userinfo.uid }}</li><br/>
        </ul>
    </div>
    <div class="history" v-loading="loading" element-loading-background="rgba(255, 255, 255,0)" element-loading-text="正在加载中">
        <h3>新闻浏览历史</h3>
        <div class="list_box">
        <ul v-for="(news,i) in news_list" :key="i" class="news_list">
        <li><span class="news_box"><a :href="news.url">{{ news.title }}</a></span><span class="visited">浏览次数:{{news.visited }}</span></li>
        </ul>
        </div>
    </div>
    
 </div>
</template>

<script>

 export default {
    name:"Userinfo_show",
    data(){
        return{
            userinfo:{
                username:'',
                mobile:'',
                email:'',
                uid:'',
            },
            news_list:[],
            loading:true,
        }
    },
    created(){
        if(window.sessionStorage.getItem('logined')!=undefined){
            let url='/userinfo/'
            this.axios.get(url,{
                responseType:'json',
            })
            .then(res=>{
                if(res.data.code==0){
                    this.userinfo.username=res.data.userinfo.username;
                    this.userinfo.mobile=res.data.userinfo.mobile;
                    this.userinfo.email=res.data.userinfo.email;
                    this.userinfo.uid=res.data.userinfo.uid;
                    this.news_list=res.data.news_list;
                    this.loading=false;
                }else{
                    console.log(res.data.errmsg);
                }
            })
            .catch(err=>{
                console.log(err);
            })
        }
    },
    methods:{

    },
 }
</script>

<style lang='less' scoped>
    *{
        background-color: rgba(255,255,255,0.5);
    }
    
    .userinfo{
        margin-top: 0%;
        width: 100%;
        height: auto;
        text-decoration-style: dashed;
        background-color: transparent!important;
        h3{
        font-weight: 530;
        margin-top: 0px;
        margin-bottom: 0px;
        };
        
        ul{
            background-color: transparent!important;
            margin-top: 15px;
            margin-bottom: 0px;
            *{
            background-color: transparent!important;
            margin-bottom: 15px;
            }
           
        }
        li{
            text-decoration: none;
            display: inline;
            
        }
        li::marker{
            content: "" ;
        }
        label{
            display: inline-block;
            width: 70px;
        }
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
    .history{
        width: 100%;
        h3{
        font-weight: 530;
        margin-top: 0px;
        margin-bottom: 5px;
        };
        .list_box{
            overflow-x: hidden;
            overflow-y: auto;
            height: 283px;
            background-color: transparent!important;
            *{
                background-color: transparent!important;
            }
            

        }
        background-color: transparent!important;
        
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
            
        };
        a{
            line-height: 0px;
            text-decoration: none;
            color: #030303;
        }
    }
};
.visited{
    line-height: 0px;
    text-align: left;
    font-size: 8px;
    display: inline;
}
</style>
