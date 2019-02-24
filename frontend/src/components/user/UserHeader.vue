<template>
  <nav class="navbar navbar-primary navbar-expand-md flex-md-nowrap bg-light d-flex"
    id="index-navbar">
    <a class="navbar-brand btn" ><i class="mx-2 fas fa-bars"></i>{{ title }}</a>
    <div class="collapse navbar-collapse">
      <ul class="navbar-nav ml-md-auto flex-row px-2">
        <li class="nav-item mx-2 px-3">
          <router-link class="nav-link btn text-primary" to="/">Home</router-link>
        </li>
        <li class="nav-item mx-2 px-3" >
          <a class="nav-link btn text-primary" @click="signout()">Sign out</a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import {toSignout} from '@/apis/apibase.js'

export default {
  'name': 'userHeader',
  props: {
    signedIn: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: "Broden Your Horizons"
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
    }
  }
}
</script>


