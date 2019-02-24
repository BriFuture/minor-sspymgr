<template>
<div id="app" class="flex-fill">
  <admin-frame title="Manager" :sidebarItems="SIDEBAR_ITEMS" :breadcrumb="breadcrumb"> 
  </admin-frame>
</div>
</template>

<script>
import AdminFrame from '@/components/UserFrame.vue'
import {isUserSignin} from '@/apis/home'

export default {
  name: 'app',
  components: {
    AdminFrame
  },
  data() {
    return {
      SIDEBAR_ITEMS: [
        { href: '/index',   name: '监控面板', icon: 'fa-home', isCurrent: true },
        { href: '/product', name: '产品', icon: 'fa-shopping-cart', isCurrent: false },
        { href: '/history', name: '历史记录', icon: 'fa-history', isCurrent: false },
        { href: '/account', name: '账户', icon: 'fa-user',  isCurrent: false },
        { href: '/setting', name: '设置', icon: 'fa-cogs', isCurrent: false },
      ],
    }
  },
  computed: {
    breadcrumb() {
      let path = this.$route.path;
      isUserSignin().then( resp => {
        if(!resp.signedIn) {
          window.location="/"
        }
      });
      // path.split
      let bread = [        
        {
          text: 'Admin',
          href: '#/index'
        } 
      ]
      let num_slash = path.match(/\//g).length; 
      if( num_slash == 1) {
        for(let side of this.SIDEBAR_ITEMS) {
          if(path.startsWith(side.href)) {
            bread.push({text: side.name, active: true})
            break;
          }
        }
      } else {
        for(let side of this.SIDEBAR_ITEMS) {
          if(path.startsWith(side.href)) {
            bread.push({text: side.name, href: `#${side.href}`})
            break;
          }
        }
        let index = path.indexOf("/", 1) + 1
        if( num_slash > 2) {
          let index2 = path.indexOf("/", index) + 1
          path = path.slice(index, index2)
        } else {
          path = path.slice(index)
        }
        bread.push({text: path, active: true})
      }
      return  bread;
    }
  },
}
</script>
