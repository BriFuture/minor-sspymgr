<template>
  <div>
    <b-card class="my-2 text-center" v-for="(item, index) in cardItems" :key="index">
      <router-link class="h3" :to="item.to">{{ item.title }}</router-link>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "adminHistory",
  data() {
    return {
      cardItems: [
        {to: "/history/order", title: "历史订单"},
        {to: "/history/email", title: "历史邮件"},
      ]
    }
  }
}
</script>

<style>

</style>
