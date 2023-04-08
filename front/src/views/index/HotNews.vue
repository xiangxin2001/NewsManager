<template>
    <div v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.3)" element-loading-text="正在加载中">
        
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
                   this.hot_news-res.data.hot_news;
                   
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
   
   </style>