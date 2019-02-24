<template>
  <nav class="navbar navbar-primary navbar-expand-md flex-md-nowrap bg-light fixed-top d-flex"
    id="index-navbar">
    <a class="navbar-brand" href="#">Get Out And Broden Your Horizons</a>
    <div class="collapse navbar-collapse">
      <ul class="navbar-nav ml-md-auto flex-row px-2">
        <li class="nav-item mx-2 px-3">
          <router-link class="nav-link btn text-primary" to="/">Home</router-link>
        </li>
        <li class="nav-item mx-2 px-3">
          <router-link class="nav-link btn text-primary" to="/signin">Sign in</router-link>
        </li>
        <li class="nav-item mx-2 px-3">
          <router-link class="nav-link btn text-success" to="/signup">Sign up</router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  'name': 'homeHeader',
  props: {
  }
}
</script>


