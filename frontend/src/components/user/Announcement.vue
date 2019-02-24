<template>
  <div>
    <b-card :title="title" :border-variant="variant" >
      <div v-html="content" ></div>
    </b-card>
  </div>
</template>

<script>
export default {
  name: 'userAnnouncementArea',
  props: {
    title: String,
    content: String,
    variant: {
      type: String,
      default: 'success'
    }
  }
}
</script>
