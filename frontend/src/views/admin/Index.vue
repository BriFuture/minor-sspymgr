<template>
<div>
  <b-button variant="success" @click="redirectAsUser()">普通用户视角</b-button>
  <b-card title="总览" class="my-1">

  </b-card>
</div>
</template>
<script>
export default {
  name: 'adminIndex',
  methods: {
    redirectAsUser() {
      window.location='/user'
    }
  }
}
</script>
