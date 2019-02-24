<template>
<div>
  <b-card>
    <div class="row">
      <div class="col-12 col-sm-9">
        <account-basic-info :accountId="account.id" :userEmail="account.email" :port="account.port" />
        <div class="row py-2">
          <div class="col-12 col-sm-4 text-left text-md">
            <text-input :input-prop="{'title': 'Host', 'icon': 'fas fa-network-wired'}"
              v-model="account.server" />
          </div>
          <div class="col-12 col-sm-4 text-left text-md">
            <text-input :input-prop="{'title': 'Password', 'icon': 'fas fa-key'}" 
              v-model="account.password" @valueChanged="isPasswordChanged = true" />
            <button type="button" class="btn btn-primary mx-2" 
              @click="updatePassword()"
              :disabled="!isPasswordChanged">{{ 'Update' }}</button>
            <button type="button" class="btn btn-primary mx-2" 
              @click="randomPassword()">{{ 'Random' }}</button>
          </div>
          <div class="col-12 col-sm-4 text-left text-md">
            <text-input :input-prop="{'title': 'TotalFlow', 'icon': 'fas fa-globe'}" 
              :value="totalFlow" @valueChanged="onFlowChanged($event)" />
            <button class="btn btn-primary mx-3" :disabled="!isFlowChanged" 
              @click="updateFlow()">{{ 'Modify' }}</button>
          </div>
        </div>
      </div>
      <div class="col-12 col-sm-3 text-center">
        <b-alert variant="primary" show>
          使用 shadowsocks 手机客户端的“扫一扫”导入配置
        </b-alert>
        <qrcode-vue :value="ssAddress" :size="200"  class="d-inline-block mx-auto"
          level="H"></qrcode-vue>
        <!-- <img src="test" width="100%" height="100%"/> -->
      </div>
    </div>
  </b-card>
  <div class="row border-bottom py-2">
    <div class="col-12 text-left text-lg">{{ 'FlowUsage:' }}
      <b-progress :max="totalFlow" class="mb-3" show-value :precision="1">
        <b-progress-bar :value="$convertFlow(accFlow.flow, 'GB')" variant="primary" >
        </b-progress-bar>
        <b-progress-bar :value="totalFlow - $convertFlow(accFlow.flow, 'GB')" variant="success" >
        </b-progress-bar>
      </b-progress>
    </div>
  </div>
  <div class="border-bottom my-2">
    <!-- {# Expire Time, followed by actions #} -->
    <div class="row pb-2" @click="showExpireModify()">
      <span class="col-4 text-left text-lg">{{ 'Expire:' }}</span>
      <span class="col-5 text-left text-md">{{ $formatTime(account.expire) }}</span>
      <button class="col-2 btn btn-primary py-0">{{ 'Modify' }}</button>
    </div>
    <div class="border border-primary mt-3" v-show="isExpireModify">
      <div class="row my-2 mx-auto">
        <button @click="modifyExpiration(-1)" value="-1"  class="btn btn-secondary col mx-3">{{ '-1d' }}</button>
        <button @click="modifyExpiration(-7)" value="-7"  class="btn btn-secondary col mx-3">{{ '-7d' }}</button>
        <button @click="modifyExpiration(-15)" value="-15" class="btn btn-secondary col mx-3">{{ '-15d' }}</button>
        <button @click="modifyExpiration(-30)" value="-30" class="btn btn-secondary col mx-3">{{ '-30d' }}</button>
        <button @click="acc_time_custom('-')" class="btn btn-success col mx-3">{{ 'Custom Sub' }}</button>
      </div>
      <div class="row my-2 mx-auto">
        <button @click="modifyExpiration(+1)" value="+1"  class="btn btn-primary col mx-3">{{ '+1d' }}</button>
        <button @click="modifyExpiration(+7)" value="+7"  class="btn btn-primary col mx-3">{{ '+7d' }}</button>
        <button @click="modifyExpiration(+15)" value="+15" class="btn btn-primary col mx-3">{{ '+15d' }}</button>
        <button @click="modifyExpiration(+30)" value="+30" class="btn btn-primary col mx-3">{{ '+30d' }}</button>
        <button @click="acc_time_custom('+')" class="btn btn-success col mx-3">{{ 'Custom Add' }}</button>
      </div>
    </div>
  </div>
  <div class="row border-bottom my-2">
    <span class="col-6 text-left text-lg">{{ 'Status:' }} </span>
    <span class="col-6 text-left text-md">{{ account.status }}</span>
  </div>
  <div class="row border-bottom my-2">
    <span class="col-6 text-left text-lg">{{ 'Create Time:' }} </span>
    <span class="col-6 text-left text-md">{{ $formatTime(account.createTime) }}</span>
  </div>
  <div class="row border-bottom my-2" v-if="account.userId">
    <span class="col-6 text-left text-lg">{{ 'Last Connected:' }} </span>
    <span class="col-6 text-left text-md">{{ $formatTime(accFlow.updateTime) }}</span>
  </div>
</div>
</template>

<script>
import { randomAccountPassword, updateAccountPassword
  , updateAccountFlow, updateAccountExpiration} from '@/apis/admin.js'
import TextInput from '@/components/TextInput.vue'
import AccountBasicInfo from '@/components/admin/AccountBasicInfo.vue'
import QrcodeVue from 'qrcode.vue'

const GB = 1024 * 1024 * 1024;
export default {
  name: 'accountDetail',
  components: {
    TextInput,
    AccountBasicInfo,
    QrcodeVue
  },
  props: {
    account: {
      type: Object,
      default: {}
    },
    accFlow: {
      type: Object,
      default: {}
    },
    ssAddress: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      isExpireModify: false,
      isPasswordChanged: false,
      isFlowChanged: false,
    }
  },
  computed: {
    totalFlow() {
      return this.account.totalFlow / GB;
    }
  },
  methods: {
    showExpireModify() {
      this.isExpireModify = ! this.isExpireModify;
    },
    modifyExpiration(exp) {
      // console.log(exp)
      updateAccountExpiration({
        port: this.account.port,
        days: exp
      }).then( resp => {
        // console.log( resp )
        this.account.expire = resp.nexpire
      })
    },
    onFlowChanged(value) {
      this.isFlowChanged = true;
      this.account.totalFlow = value * GB;
    },
    updateFlow() {
      updateAccountFlow({
        'port': this.account.port,
        'flow': this.account.totalFlow,
        'flowUnit': 1
      }).then( resp => {
        // console.log( resp );
        this.isFlowChanged = false;
      })
    },
    updatePassword(pw) {
      // pw = 'ATEST564';
      updateAccountPassword({
        password: this.account.password, 
        port: this.account.port
      }).then( resp => {
        // console.log(resp)
        // this.account.password = pw;
        this.isPasswordChanged = false;
      })
    },
    randomPassword() {
      randomAccountPassword({
        'port': this.account.port
      }).then( resp => {
        // console.log(resp)
        if( resp.status === 'success'){
          this.account.password = resp.password;
          this.isFlowChanged = false;
        }
      })
    }
  },
}
</script>
