<template><div>
 <a href="/"><div class="logo" ></div></a>
 </div>
</template>

<script>
 export default {
    name:"Logo"
 }
</script>

<style lang='less' scoped>
.logo{
    margin-left: 0px;
    margin-top: 0px;
    height: 70px;
    width: 200px;
    background-image: url(../../public/img/logo.png);
    background-repeat: no-repeat;
    background-position: left top;
    align-items: top;
    display: inline-block;
}
</style>