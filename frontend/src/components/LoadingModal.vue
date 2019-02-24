<template>
<b-modal :title="title" :visible="loading" :ok-only="true">
  <div>
    <a-spin size="large">loading</a-spin>
  </div>
</b-modal>
</template>

<script>
export default {
  name: 'loadingModal',
  props: {
    title: {
      type: String,
      default: "加载数据中"
    },
    loading: {
      type: Boolean,
      default: true
    }
  },
  model: {
    prop: 'loading',
    
  }
}
</script>
