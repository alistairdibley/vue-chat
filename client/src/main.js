import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueSocketio from 'vue-socket.io';
import io from 'socket.io-client';
import BootstrapVue from 'bootstrap-vue'
import store from "./store";
Vue.use(BootstrapVue)

const socketInstance = io('http://127.0.0.1:8000/test', {
  transports: ['websocket'],
});
// const socketInstance = io('http://127.0.0.1:8000/test');
// Vue.use(VueSocketio, 'http://192.168.2.114:8000/test', {transports:['websocket']});
Vue.use(VueSocketio, socketInstance)
Vue.config.productionTip = false
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
