import '../common'
import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);

const routers = [
  { path: '/', name: 'index', component: 'Index', alias: ['/index'] },
  { path: '/product', name: 'product', component: 'Product' },
  { path: '/product/:id', name: 'productDetail', component: 'ProductDetail' },
  
  { path: '/history', name: 'history', component: 'History' },
  { path: '/history/email', name: 'emailHistory', component: 'histories/Email' },
  { path: '/history/order', name: 'orderHistory', component: 'histories/Order' },
  { path: '/history/order/:id', name: 'orderHistoryDetail', component: 'histories/OrderDetail' },
  // { path: '/user', name: 'user', component: 'User' },
  { path: '/user/:id', name: 'userDetail', component: 'UserDetail' },
  { path: '/email', name: 'email', component: 'Email' },
  { path: '/account', name: 'account', component: 'Account' },
  { path: '/account/:id', name: 'accountDetail', component: 'AccountDetail' },
  { path: '/setting', name: 'setting', component: 'Setting' },
  { path: '/setting/announcement', name: 'announcement', component: 'settings/Announcements' },
  { path: '/setting/webserver', name: 'webserver', component: 'settings/Websetting' },
];

const routes = routers.map( route => {
  return {
    ...route,
    component: () => import(`@/views/admin/${route.component}.vue`)
  }
})

const router = new VueRouter({
  routes,
  mode: 'hash'
});

import App from './App.vue'
new Vue({
  router,
  render(h){
    return h(App)
  }
}).$mount('#app')