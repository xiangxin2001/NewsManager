import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
axios.interceptors.request.use((config) => {
    config.baseURL="http://newsmanager.com:8000";
    config.headers['X-Requested-With'] = 'XMLHttpRequest';
    let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
    config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1];
    return config
});
Vue.use(VueAxios, axios) 