<template>
  <div>
    <div class="row border-bottom py-2">
      <div class="col-12 col-sm-4 text-left text-md">
        <text-input :input-prop="{'title': 'Account', 'icon': 'fas fa-user-circle'}"
          :readonly="true"
          v-model="accountId" />
      </div>
      <div class="col-12 col-sm-4 text-left text-md">
        <text-input :input-prop="{'title': 'Belongs To:', 'icon': 'far fa-user'}"
          :readonly="true"
          v-model="userEmail" />
      </div>
      <div class="col-12 col-sm-4 text-left text-md">
        <text-input :input-prop="{'title': 'Port', 'icon': 'fas fa-ethernet'}"
          :readonly="true"
          v-model="port" />
      </div>
    </div>
  </div>
</template>

<script>
import TextInput from '@/components/TextInput.vue'
export default {
  name: 'accountBasicInfo',
  components: {
    TextInput
  },
  props: {
    accountId: Number,
    userEmail: String,
    port: Number
  },

}
</script>

