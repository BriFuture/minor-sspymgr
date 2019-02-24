<template>
<div>
  <b-card-group deck>
    <b-card class="col-12 col-sm-8" title="修改登录密码">
      <update-password />
    </b-card>
  </b-card-group>
</div>
</template>

<script>
import UpdatePassword from '@/components/UserUpdatePassword.vue'
export default {
  name: 'userSetting',
  components: {
    UpdatePassword
  }
}
</script>

