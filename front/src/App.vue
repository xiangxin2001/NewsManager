<template>
  <div id="app">
    
    <router-view>
      
    </router-view>
  </div>
</template>

<script>

export default {
  name: 'app',
  components: {
 
  },
  mounted(){
    
    this.axios.get('/get_token', {
        responseType: 'json',
    })
    .then(res=>{
        let csrf_token = res.data.csrf_token
        window.sessionStorage.setItem("csrf_token", csrf_token)
    })
    .catch(error => {
        console.log(error)
    })
    
  }
}
</script>

<style>
.el-pagination.is-background .el-pager li:not(.disabled) {
    background-color: rgba(0,0,0,0);   
    color: #060606;
  }
.el-pagination.is-background .el-pager li:not(.disabled).active {
    background-color: rgba(57, 222, 156, 0.9);  
    color: #fff;
}

</style>
