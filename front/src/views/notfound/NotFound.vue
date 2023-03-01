<template>
    <div class="notfound">
        <logo></logo>
        <img src="../../../public/img/404.png" alt="">
    </div>

</template>
<script>
import Logo from'@/components/Logo.vue'
export default {
    name:"NotFound",
    components:{
      logo:Logo
    }
}
</script  >
<style lang="less" scoped>
.notfound{
    width: 100%;
    height: 100%;
    overflow: hidden;
}
.notfound img{
    margin-left: 25%;
    width: 50%;
    height: 50%;
    display: flex;
}
</style>