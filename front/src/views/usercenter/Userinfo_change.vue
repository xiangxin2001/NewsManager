!<template>
 <div class="back">
    <el-select v-model="value" placeholder="请选择要修改的内容" style="margin-left: 40%;">
        <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value">
        </el-option>
    </el-select>
    <Password v-if="value=='1'"></Password>
    <Username v-if="value=='2'"></Username>
    <Mobile v-if="value=='3'"></Mobile>
    <Email v-if="value=='4'"></Email>
    <Reset v-if="value=='5'"></Reset>
 </div>
</template>

<script>
import Password from '@/views/usercenter/Passoword.vue';
import Username from '@/views/usercenter/Username.vue';
import Mobile from '@/views/usercenter/Mobile.vue';
import Email from '@/views/usercenter/Email.vue';
import Reset from'@/views/usercenter/Reset.vue';
export default {
components:{
    Password,Username,Mobile,Email,Reset
},
data() {

    return {
        options: [{
            value: '1',
            label: '密码修改'
            }, {
            value: '2',
            label: '用户名修改'
            }, {
            value: '3',
            label: '手机号修改'
            }, {
            value: '4',
            label: '邮箱修改'
            }, {
            value: '5',
            label: '重置账号'
            }
        ],
        value:'1',
    }; 
},
}
</script>

<style lang='less' scoped>
.back{
    background-color: rgba(255,255,255,0.5);
    *:not(.el-button){
        background-color: transparent !important;
    }
        
}


/deep/.el-input__inner{
    border: 1px solid #737377;
    margin-top: 5px;
}
/deep/.el-select .el-input .el-select__caret {
    color:  #737377;
}
/deep/.el-input .el-input__inner::placeholder {
    color:rgba(0,0,0, 0.7);
}
/deep/.el-select .el-input.is-focus .el-input__inner::placeholder{
    color:rgba(0,0,0,0.3);
}
.el-select-dropdown__item.hover{
    background-color: rgba(200, 200, 200, 0.5);
}

</style>