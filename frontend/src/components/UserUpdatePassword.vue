<template>
  <div>
    <b-form class="form needs-validation" role="form" autocomplete="off" id="formSignin" novalidate method="post">
      <b-form-group :state="oldState" :invalid-feedback="oldHint">
        <b-input-group>
          <label for="oldPassword" class="my-auto mr-2">{{ '旧密码：' }}</label>
          <b-form-input type="password" id="oldPassword" class="form-control" 
            placeholder="旧密码" required="" 
            :state="oldState" v-model="oldPassword" />
        </b-input-group>
      </b-form-group>
      <b-form-group :state="newState" :invalid-feedback="newHint">
        <b-input-group>
          <label for="newPassword" class="my-auto mr-2">{{ '新密码：' }}</label>
          <b-form-input :type="pwInputType" id="newPassword"
            v-model="newPassword" :state="newState"
            placeholder="New Password" required="" />
          <b-form-checkbox class="my-auto ml-3" @change="showNewPassword()">
            {{ '显示新密码' }}
          </b-form-checkbox>
        </b-input-group>
      </b-form-group>
      <b-form-group>
        <b-button variant="primary" class="btn-lg mx-auto" :disabled="!canUpdate" 
          type="button" id="updateBtn" @click="toUpdatePassword()">{{ 'Update' }}</b-button>
      </b-form-group>
    </b-form>
    <b-modal title="修改密码" v-model="passwordModal" :ok-only="true">
      <div class="text-success text-lg">成功修改密码</div>
    </b-modal>
  </div>
</template>

<script>
import {updateUserPassword} from '@/apis/user'
export default {
  name: 'userUpdatePassword',
  data() {
    return {
      oldPassword: null,
      newPassword: null,
      oldState: null,
      oldHint: "",
      newHint: "输入新密码",
      pwInputType: "password",
      passwordModal: false
    }
  },
  computed: {
    newState() {
      if(this.newPassword === null) {
        return null;
      }
      
      return this.newPassword.length > 5 ? true : false;
    },
    canUpdate() {
      if(this.newState && this.oldPassword !== null) {
        return true;  
      } 
      return false;
    }
  },
  methods: {
    showNewPassword() {
      if( this.pwInputType === 'password')
        this.pwInputType = "text"
      else
        this.pwInputType = "password"
    },
    toUpdatePassword() {
      this.oldState = null;
      updateUserPassword({ 
        oldPassword: this.oldPassword,
        newPassword: this.newPassword
      }).then( resp => {
        if( resp === 'success') {
          this.passwordModal = true
        } else {
          this.oldState = false;
          this.oldHint = "密码错误"
        }
      })
    }
  }
}
</script>
