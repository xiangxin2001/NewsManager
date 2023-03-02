import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
axios.defaults.xsrfCookieName = 'csrfmiddlewaretoken';
axios.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';
axios.defaults.withCredentials = true;
axios.defaults.baseURL="https://newsmanager.com:8000";
axios.interceptors.request.use(config => {
    config.headers['X-Requested-With'] = 'XMLHttpRequest';
    
    // let regex = /.*csrftoken=([^;.]*).*$/; // 用于从cookie中匹配 csrftoken值
    // console.log(document.cookie)
    config.headers['X-CSRFToken'] =  window.sessionStorage.getItem("csrf_token");
    return config
  }, err => {
    // 请求未成功发出，如：没有网络...
    return Promise.reject(err)
  })
Vue.use(VueAxios, axios) 