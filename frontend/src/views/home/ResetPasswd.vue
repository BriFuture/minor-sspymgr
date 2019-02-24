<template>
<div>
  <div class="card rounded-0 text-left form-signin">
    <div class="card-header">
      <h3 class="mb-0">重置密码</h3>
    </div>
    <div class="card-body">
      <div>
        <span class="text-lg text-primary my-2"></span>
        <form class="form needs-validation my-2" method="POST">
          <b-form-group label="输入新密码" label-for="newPassword"
            :state="resetState"
            invalid-feedback="密码长度过短，至少需要 6 个字符">
            <b-form-input type="password" 
              id="newPassword"
              :state="resetState" 
              v-model="newpw" required="" />
          </b-form-group>
          <b-form-group>
              <b-button variant="primary" type="button" 
                :disabled="resetState !== true"
                @click="reset()" >{{ 'Reset' }}
              </b-button>
          </b-form-group>
        </form>
      </div>
    </div>
  </div>
  <b-modal v-model="hint" :hide-footer="responseText === null" 
    :ok-only="true" :no-close-on-backdrop="true" title="修改密码">
    <div v-if="responseText === null">
      请稍候。
    </div>
    <div v-else-if="responseText.length === 0">
      <span class="text-lg text-primary">修改密码成功</span>
      <router-link class="d-block" to="/signin"><b-button variant="success" >{{ 'Return to signin page' }}</b-button></router-link>
    </div>
    <div v-else>
      <span class="text-lg text-primary">修改密码失败，修改请求无效或请求已过期</span>
    </div>
  </b-modal>
</div>
</template>

<script>
import {resetPassword} from '@/apis/home'

export default {
  name: 'doResetPassword',
  data() {
    return {
        stage: 'email',
        hint: false,
        newpw: null,
        responseText: null,
    }
  },
  computed: {
    resetState() {
      if(this.newpw === null) {
        return null;
      }
      return this.newpw.length > 5 ? true : false;
    },
    resetCode() {
      let li = this.$route.path.lastIndexOf('/') + 1
      return this.$route.path.slice(li)
    },

  },
  methods: {
    reset() {
      if(this.resetState !== true) {
        return;
      }
      this.responseText = null;
      resetPassword({code: this.resetCode, newPassword: this.newpw}).then(
        resp => {
          this.responseText = ''
          if( resp.status === 'fail')
            this.responseText = resp.hint
          this.hint = true;

        }
      )
    }
  },

}
</script>

<style>

</style>

