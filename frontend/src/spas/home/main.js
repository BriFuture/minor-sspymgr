import '../common'
import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import $http from 'jquery'
Vue.prototype.$http = $http

const routers = [
  { 
    path: '/', name: 'index', component: 'Signin',
    meta: {
      title: 'Home Page - SSPYMGR',
      metaTags: [
        {
          name: 'description',
          content: 'The signin page of SSPYMGR.'
        },
        {
          property: 'og:description',
          content: 'The home page of our example app.'
        }
      ]
    },
    alias: ['/signin', '/index'],
  },
  // { path: '/signin', name: 'signin', component: Signin },
  { path: '/signup', name: 'signup', component: 'Signup' },
  { path: '/resetPassword', name: 'requestReset', component: 'ResetPassword' },
  { path: '/resetPassword/:id', name: 'resetPassword', component: 'ResetPasswd' },
]

const routes = routers.map( route => {
  return {
    ...route,
    component: () => import(`@/views/home/${route.component}.vue`)
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
  // components: { App },
  // template: '<App/>'
}).$mount('#app')