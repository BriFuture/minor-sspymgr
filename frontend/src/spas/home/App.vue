<template>
  <div id="app" class="page">
    <home-header :signed-in="signedIn" />
    <router-view></router-view>
  </div>
</template>

<script>
import HomeHeader from '@/components/HomeHeader.vue'
import {isUserSignin} from '@/apis/home.js'
export default {
  name: 'app',
  components: {
    HomeHeader
  },
  data() {
    return {
      signedIn: false
    }
  },
  methods: {
    isSignedIn() {
      isUserSignin().then( resp => {
        if( resp.signedIn ) {
          if( resp.level === 'admin') {
            // this.$router.replace('/admin')
            window.location = '/admin'
          } else {
            window.location = '/user'
            // this.$router.replace('/admin')
          }
        }
      })
    },
  },
  created() {
    this.isSignedIn();
  }
}
</script>

<style>
body {
    direction: ltr;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    -webkit-tap-highlight-color: transparent;
    -webkit-text-size-adjust: none;
    -ms-touch-action: manipulation;
    touch-action: manipulation;
    -webkit-font-feature-settings: "liga" 0;
    font-feature-settings: "liga" 0;
    height: 100%;
    overflow-y: scroll;
    position: relative;
    background-color: #f0f0f0;
}

.page {
    margin-top: 20px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-direction: column;
    flex-direction: column;
    -ms-flex-pack: center;
    justify-content: center;
    min-height: 100%;
}
</style>
