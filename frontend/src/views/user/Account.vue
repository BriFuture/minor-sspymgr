<template>
<div>
  <b-card>
    <div class="row">
      <div class="col-12 col-sm-8">
        <div class="row border-bottom py-2">
          <div class="col-12 col-sm-6 text-left text-md">
            <text-input :input-prop="{'title': 'Host', 'icon': 'fas fa-network-wired'}"
              :readonly="true"
              v-model="ad.server" />
          </div>
          <div class="col-12 col-sm-6 text-left text-md">
          <text-input :input-prop="{'title': 'Port', 'icon': 'fas fa-ethernet'}"
            :readonly="true"
            v-model="ad.port" />
          </div>
        </div>
        <div class="row py-2">
          <div class="col-12 col-sm-6 text-left text-md">
            <text-input :input-prop="{'title': 'Password', 'icon': 'fas fa-key'}" 
              v-model="ad.password" @valueChanged="isPasswordChanged = true" />
            <button type="button" class="btn btn-primary mx-3" 
              @click="updatePassword()"
              :disabled="!isPasswordChanged">{{ 'Update' }}</button>
          </div>
          <div class="col-12 col-sm-6 text-left text-md">
            <text-input :input-prop="{'title': 'TotalFlow', 'icon': 'fas fa-globe'}" 
              :readonly="true"
              :value="totalFlow.toFixed(0) + ' GB'"/>
            <span>{{ 'FlowUsage:' }}</span>
            <b-progress :max="totalFlow" class="mb-3" show-value :precision="1">
              <b-progress-bar :value="$convertFlow(ad.usedFlow, 'GB')" variant="primary" >
              </b-progress-bar>
              <b-progress-bar :value="totalFlow - $convertFlow(ad.usedFlow, 'GB')" variant="success" >
              </b-progress-bar>
            </b-progress>
          </div>
        </div>
      </div>
      <div class="col-12 col-sm-4 text-center">
        <b-alert variant="primary" show>
          使用 shadowsocks 手机客户端的“扫一扫”导入配置
        </b-alert>
        <qrcode-vue :value="ssAddress" :size="200"  class="d-inline-block mx-auto"
          level="H"></qrcode-vue>
        <!-- <img src="test" width="100%" height="100%"/> -->
      </div>
    </div>
  </b-card>
  <b-card>
    <div class="border-bottom my-2">
      <!-- {# Expire Time, followed by actions #} -->
      <div class="row pb-2">
        <span class="col-4 text-left text-lg">{{ 'Expire:' }}</span>
        <span class="col-8 text-left text-md">{{ $formatTime(ad.expire) }}</span>
      </div>
    </div>
    <div class="row border-bottom my-2">
      <span class="col-4 text-left text-lg">{{ 'Status:' }} </span>
      <span class="col-4 text-left text-md">{{ ad.status }}</span>
    </div>
    <div class="row border-bottom my-2">
      <span class="col-4 text-left text-lg">{{ 'Create Time:' }} </span>
      <span class="col-8 text-left text-md">{{ $formatTime(ad.createTime) }}</span>
    </div>
    <div class="row my-2" v-if="ad.userId">
      <span class="col-4 text-left text-lg">{{ 'Last Connected:' }} </span>
      <span class="col-8 text-left text-md">{{ $formatTime(ad.updateTime) }}</span>
    </div>
  </b-card>
  <b-modal v-model="modifyPasswordModal" :ok-only="true" title="修改密码状态">
    修改成功
  </b-modal>
</div>
</template>

<script>
import TextInput from '@/components/TextInput.vue'
import {getUserAccount, updateAccountPassword} from '@/apis/user.js'
import QrcodeVue from 'qrcode.vue'

const GB = 1024 * 1024 * 1024;

export default {
  name: 'userIndex',
  components: {
    TextInput,
    QrcodeVue
  },
  data() {
    return {
      ad: {},
      ssAddress: "",
      isPasswordChanged: false,
      modifyPasswordModal: false,
    }
  },
  methods: {
    updatePassword(pw) {
      // console.log(this.ad.password)
      updateAccountPassword({
        password: this.ad.password, 
      }).then( resp => {
        this.modifyPasswordModal = true;
        // this.ad.password = pw;
        this.isPasswordChanged = false;
      })
    },
  },
  computed: {
    totalFlow() {
      return (this.ad.totalFlow / GB);
    }
  },
  created() {
    getUserAccount().then( resp => {
      console.log(resp)
      this.ad = resp.account;
      this.ssAddress = "ss://" +btoa(resp.ssAddress);
    })
  }
}
</script>
