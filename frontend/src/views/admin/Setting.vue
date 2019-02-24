<template>
<div>
  <div>
    <b-card class="my-2 text-center" v-for="(item, index) in cardItems" :key="index">
      <router-link class="h3" :to="item.to">{{ item.title }}</router-link>
    </b-card>
  </div>
</div>
</template>

<script>
import CreateAnnouncement from '@/components/admin/CreateAnnouncement'

export default {
  name: 'adminSetting',
  components: {
    CreateAnnouncement
  },
  data() {
    return {
      settings: [],
      cardItems: [
        {to: "/setting/announcement", title: "公告"},
        {to: "/setting/webserver", title: "服务器设置"},
      ]
    }
  },
  methods: {
    switchSetting(s) {
 
    }
  },
  created() {
 
  }
}
</script>

<style>
.custom-switch {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    cursor: default;
    display: -ms-inline-flexbox;
    display: inline-flex;
    -ms-flex-align: center;
    align-items: center;
    margin: 0;
}

.custom-switch-input {
    position: absolute;
    z-index: -1;
    opacity: 0;
}

.custom-switch-indicator {
    display: inline-block;
    height: 1.25rem;
    width: 2.25rem;
    background: #e9ecef;
    border-radius: 50px;
    position: relative;
    vertical-align: bottom;
    border: 1px solid rgba(0, 40, 100, 0.12);
    transition: .3s border-color, .3s background-color;
}

input[type="radio"], input[type="checkbox"] {
    box-sizing: border-box;
    padding: 0;
}
</style>
