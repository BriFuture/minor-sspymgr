import '../common'
import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);

const routers = [
  { 
    path: '/', 
    name: 'index', 
    component: 'Index',
    meta: {
      title: 'User Home Page - SSPYMGR',
      metaTags: [
        {
          name: 'description',
          content: 'The User home page of SSPYMGR.'
        },
        {
          property: 'og:description',
          content: 'The home page of our example app.'
        }
      ]
    },
    alias: ['/index'],
  },
  { path: '/account', name: 'account', component: 'Account' },
  { path: '/product', name: 'product', component: 'Product' },
  { path: '/product/:id', name: 'productDetail', component: 'ProductDetail' },
  { path: '/orderHistory', name: 'orderHistory', component: 'OrderHistory' },
  { path: '/setting', name: 'setting', component: 'Setting' },
];
  
const routes = routers.map( route => {
  return {
    ...route,
    component: () => import(`@/views/user/${route.component}.vue`)
  }
})

const router = new VueRouter({
  routes,
  mode: 'hash'
});

import App from './App.vue'

new Vue({
  router,
  render(h) {
    return h(App)
  }
}).$mount('#app')