<template>
  <nav class="col-md-2 d-none d-md-block bg-light sidebar px-0">
    <div class="sidebar-sticky">
      <ul class="nav flex-column">
        <li class="nav-item mt-1" v-for="(item, index) in items" :key="index"
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
</template>

<script>
export default {
  'name': 'settingSidebar',
  props: {
    items: Array
  },
  methods: {
    itemClicked( item ) {
      for( let it of this.items ) {
        it.isCurrent = false;
      }
      item.isCurrent = true;
      this.$emit( 'itemChanged', item.name )
      this.$router.push( { path: item.href } )
    },
    updateCurrentItem() {
      let name = null;
      if( this.$route.path === '/' ) {
        this.items[0].isCurrent = true;
      } else {
        let path = this.$route.path
        let index = path.indexOf('/', 1)
        if( index > 0 ) {  
          path = path.slice(0, index);
        }
        for( let it of this.items ) {
          if( path === it.href ) {
            it.isCurrent = true;
            name = it.name;
          } else {
            it.isCurrent = false;
          }
        }
        this.$emit( 'itemChanged', name )
      }
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
    min-height: calc(100vh - 20px);
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

