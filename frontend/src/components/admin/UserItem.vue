<template>
<div>
  <div class="row">
    <b-form-group class="col-12 col-sm-6" >
      <label>邮箱：</label>
      <b-form-input  
        :readonly="true" :value="user.email">
      </b-form-input>
    </b-form-group>
    <b-form-group class="col-12 col-sm-6">
      <label>类型：</label>
      <b-form-select v-model="user.type" @change="applyStatusChanged()">
        <option :value="null">空白</option>
        <option value="notified">邮件通知过</option>
        <option value="active">已激活</option>
        <option value="banned">已禁用</option>
      </b-form-select>
    </b-form-group>
    <b-form-group class="col-12 col-sm-6" >
      <label>用户名：</label>
      <b-form-input  
        :readonly="true" :value="user.username">
      </b-form-input>
    </b-form-group>
    <b-form-group class="col-12 col-sm-6" >
      <label>备注：</label>
      <b-form-input  
        v-model="user.comment" @input="applyStatusChanged()">
      </b-form-input>
    </b-form-group>
  </div>
  <b-button class="float-right" :variant="applyStatus" @click="applyChanges()">应用</b-button>
</div>
</template>

<script>
import {updateUserBasicInfo} from '@/apis/admin'

export default {
  name: 'userItem',
  props: {
    user: {
      type: Object,
      default: {}
    },
  },
  data() {
    return {
      applyStatus: "secondary"
    }
  },
  methods: {
    applyStatusChanged() {
      this.applyStatus = "primary";
    },
    applyChanges() {
      updateUserBasicInfo( {
        userId: this.user.id,
        comment: this.user.comment,
        type: this.user.type
      }).then( resp => {
        this.applyStatus = "secondary";
        console.log(resp);
      })
    }
  },
  created() {
    this.applyStatus = "secondary";
  }
}
</script>
