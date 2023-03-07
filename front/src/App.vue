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

<style lang="less">
.el-pagination.is-background .el-pager li:not(.disabled) {
    background-color: rgba(255, 255, 255, 0);   
    color: #060606;
}

.el-textarea__inner,.el-input__inner {
    background:  rgba(255, 255, 255, 0) !important;
    border: #060606;
    
}
.el-menu{
    padding: 0px;
    background-color: rgba(255, 255, 255, 0.5)!important;
    div{
      :hover{
        background-color:rgba(255, 255, 255, 1)!important;
      }
    }
    
}
.el-menu-item{
  background-color: transparent!important;
  :hover{
    background-color:rgba(255, 255, 255, 1)!important;
  }
}
.el-pagination.is-background .btn-next, .el-pagination.is-background .btn-prev, .el-pagination.is-background .el-pager li{
  background-color: rgba(255, 255, 255, 0.2)!important;
 
}
</style>
