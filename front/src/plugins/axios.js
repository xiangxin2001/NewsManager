import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
axios.defaults.xsrfCookieName = 'csrfmiddlewaretoken';
axios.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';
axios.defaults.withCredentials = true;
axios.defaults.baseURL="https://newsmanager.com:8000";
axios.interceptors.request.use(config => {
    config.headers['X-Requested-With'] = 'XMLHttpRequest';
    
    config.headers['X-CSRFToken'] =  window.sessionStorage.getItem("csrf_token");
    return config
  }, err => {
    // 请求未成功发出
    return Promise.reject(err)
  })
Vue.use(VueAxios, axios) 