<template>
<div>
  <div class="my-2">
    <b-button variant="primary" @click="$router.go(-1)">
      {{ '返回' }}
    </b-button>
  </div>
  <b-card class="my-2" title="网站用户信息">
    <user-item :user="user" />
  </b-card>
  <b-card class="my-2" title="SS账户信息">
    <account-item :account="ad" :ssAddress="ssAddress" :accFlow="accFlow" />
  </b-card>
  <b-card title="流量日统计">
    <day-flow-usage ref="flowUsage" @selectDate="changeFlowDate($event)" />
  </b-card>
</div>
</template>

<script>
import { getAccountDetail, getUserDetail,
getDayFlowUsage, getMonFlowUsage } from '@/apis/admin.js'
import TextInput from '@/components/TextInput.vue'

import AccountItem from '@/components/admin/AccountItem'
import UserItem from '@/components/admin/UserItem'
import DayFlowUsage from '@/components/DayFlowUsage'

export default {
  name: 'accountDetail',
  components: {
    TextInput,
    AccountItem,
    UserItem,
    DayFlowUsage
  },
  data() {
    return {
      ad: {},
      accFlow: {},
      user: {},
      ssAddress: "",
    }
  },
  methods: {
    changeFlowDate(day) {
      let id = this.$route.params.id;
      getDayFlowUsage({
        accountId: id,
        date: day.format("YYYY-MM-DD")
      }).then( resp => {
        // this.chartData.rows = resp.records;
        this.$refs.flowUsage.setRecords(resp.records)
        this.$refs.flowUsage.setDate(resp.date*1000)
      })
    }
  },
  created() {
    let id = this.$route.params.id;
    getAccountDetail({id: id}).then( resp => {
      if( resp.status === 'success' ) {
        // console.log(resp)
        this.ad = resp.account;
        this.ad.email = resp.user.email;
        this.accFlow = resp.accountFlow;
        this.user = resp.user;
        this.ssAddress = "ss://" + btoa(resp.ssAddress);
      }
    });
    this.changeFlowDate(this.$moment())
  }
}
</script>
