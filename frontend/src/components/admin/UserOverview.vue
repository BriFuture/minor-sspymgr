<template>
<div class="table-responsive">
  <b-table striped hoverd :items="users" :fields="fields">
    <template slot="flow" slot-scope="data">
      {{$formatFlow(data.value, "MB")}}
    </template>
    <template slot="price" slot-scope="data">
      ￥{{data.value}}
    </template>
    <template slot="action" slot-scope="row">
      <b-button variant="primary" @click="$emit('actionClicked', row.item.id)">操作</b-button>
    </template>
  </b-table>
</div>
</template>

<script>
import {getAllUser} from '@/apis/admin.js'
export default {
  name: 'adminUser',
  props: {
    users: Array,
  },
  data() {
    return {
      fields: [
        { key: 'id', label: "User ID" },
        { key: 'email', label: "邮箱" },
        { key: 'type', label: "类型" },
        { key: 'comment', label: "备注" },
        { key: 'username', label: "用户名" },
        { key: 'createTime', label: "创建日期", formatter: this.$formatTime },
        { key: 'action', label: "操作" },
      ]
    }
  }
}
</script>

