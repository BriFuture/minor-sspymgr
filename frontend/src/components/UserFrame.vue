<template>
<div>
  <nav class="navbar navbar-primary navbar-expand-md flex-md-nowrap bg-dark d-flex"
    id="index-navbar">
    <a class="navbar-brand btn text-white" @click="showSidebar()">
      <i class="mx-2 fas fa-bars d-md-inline-block d-none"></i>
      <i class="mx-2 fas fa-bars d-md-none" :class="{ 'fa-times': isSidebarShow}"></i>
      {{ title }}
    </a>
    <div class="collapse navbar-collapse">
      <ul class="navbar-nav ml-md-auto flex-row px-2">
        <li class="nav-item mx-2 px-3">
          <router-link class="nav-link btn btn-primary" to="/">Home</router-link>
        </li>
        <li class="nav-item mx-2 px-3" >
          <a class="nav-link btn btn-primary text-white" @click="signout()">Sign out</a>
        </li>
      </ul>
    </div>
  </nav>
  <div class="container-fluid flex-fill">
    <div class="row flex-fill">
      <nav class="col-md-2 d-md-block bg-light sidebar px-0 col-8" :class="{ 'd-none': !isSidebarShow}">
        <div class="sidebar-sticky">
          <ul class="nav flex-column">
            <li class="nav-item mt-1" v-for="(item, index) in sidebarItems" :key="index"
              @click="itemClicked( item )" 
              >
              <span class="nav-link text-md" 
                :class="{ 'bg-success': item.isCurrent, 'text-white': item.isCurrent, 'text-primary': !item.isCurrent }">
                <i class="fas" :class="item.icon"></i>
                <span class="ml-3">{{ item.name }}</span>
              </span>
            </li>
          </ul>
        </div>
      </nav>
      <main role="main" class="col-md-10 col-12 ml-sm-auto pt-1 px-2">
        <div><b-breadcrumb :items="breadcrumb"></b-breadcrumb></div>
        <router-view></router-view>
      </main>
    </div>
  </div>
</div>
</template>

<script>
import {toSignout} from '@/apis/apibase.js'

export default {
  'name': 'userFrame',
  props: {
    signedIn: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: "Broden Your Horizons"
    },
    sidebarItems: Array,
    breadcrumb: Array,
  },
  data() {
    return {
      isSidebarShow: false
    }
  },
  methods: {
    signout() {
      toSignout().then( resp => {
        console.log( resp )
        if(resp === 'success') {
          window.location = '/'
        }
      })
    },
    itemClicked( item ) {
      for( let it of this.sidebarItems ) {
        it.isCurrent = false;
      }
      item.isCurrent = true;
      this.$emit( 'itemChanged', item.name )
      this.$router.push( { path: item.href } )
    },
    updateCurrentItem() {
      let name = null;
      if( this.$route.path === '/' ) {
        for( let it of this.sidebarItems ) {
            it.isCurrent = false;
        }
        this.sidebarItems[0].isCurrent = true;
      } else {
        let path = this.$route.path
        let index = path.indexOf('/', 1)
        if( index > 0 ) {  
          path = path.slice(0, index);
        }
        for( let it of this.sidebarItems ) {
          if( path === it.href ) {
            it.isCurrent = true;
            name = it.name;
          } else {
            it.isCurrent = false;
          }
        }
        this.$emit( 'sideItemChanged', name )
      }
    },
    showSidebar() {
      this.isSidebarShow = !this.isSidebarShow;
    }
  },
  created() {
    this.updateCurrentItem()
  },
  watch: {
    $route(to, from) {
      this.updateCurrentItem()
    }
  }
}
</script>

<style>
.nav-link {
  cursor: pointer;
}
.h-100 {
  height: 100% !important;
}
.sidebar{
    background-color: #f5f5f5;
    padding-right: 20px;
    padding-top: 20px;
    min-height: calc(95vh - 30px);
}

/* On smaller screens, where height is less than 450px, change the style of the sidenav (less padding and a smaller font size) */
@media screen and (max-width: 768px) {
  .sidebar {
    padding-top: 15px;
    padding-right: 15px;
    position: fixed;
    z-index: 1000;
  }

}
</style>

