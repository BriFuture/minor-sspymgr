<template>
<div class="card-deck">
  <div class="card  rounded-0 text-left form-signin">
    <div class="card-header">
      <h3 class="mb-0">重置密码</h3>
    </div>
    <div class="card-body">
      <form class="form needs-validation" method="POST">
        <b-form-group role="group" label="输入邮箱:" label-for="resetPassword">
          <b-form-input type="email" id="resetPassword" 
            placeholder="Input Your Email" required="" 
            :state="resetState"
            v-model="email" />
          <b-form-invalid-feedback>
            输入正确的邮箱
          </b-form-invalid-feedback>
        </b-form-group><!-- /input-group -->
        <b-form-group>
          <b-button type="button" 
            :disabled="resetState !== true"
            variant="primary"
            @click="requestReset()">
            {{ 'Send Reset Request' }}
          </b-button>
        </b-form-group>
      </form>
    </div>
  </div>
  <b-modal v-model="hint" :ok-only="true" title="重置密码">
    <div slot="modal-header">提示： </div>
    <div v-if="responseText.length > 0">
      {{ responseText }}
    </div>
    <div v-else>
      请稍候。
    </div>
  </b-modal>
</div>
</template>

<script>
import {requestReset} from '@/apis/home'

export default {
  name: 'requestReset',
  data() {
    return {
      stage: 'email',
      hint: false,
      email: null,
      responseText: '',
    }
  },
  computed: {
    resetState() {
      if(this.email === null) {
        return null;
      }
      if(this.email.indexOf("@") > 0 && this.email.indexOf(".") > 0) {
        return true;
      }
      return false;
    }
  },
  methods: {
    requestReset() {
      if(this.resetState === true) {
        this.hint = true;
        this.responseText = ''
        requestReset({
          email: this.email 
        }).then( resp => {
          console.log(resp)
          if(resp.status === 'success') {
            this.responseText = '重置密码链接发送成功，请检查你的邮箱。'
          } else {
            this.responseText = '重置密码链接发送失败，填写的邮箱错误。'
          }
        });
      }
    }
  },
  created() {
    // stage
  }
}
</script>

<style>

</style>

