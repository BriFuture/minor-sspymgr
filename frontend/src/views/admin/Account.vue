<template>
<b-card no-body>
  <b-tabs card>
    <b-tab title="SS 账户" active>
      <div class="table-responsive">
        <div class="my-2">
          <button class="btn btn-primary" data-toggle="modal" onclick="show_add_account()">{{ 'Add New Account' }}</button>
        </div>
        <b-table striped hover :items="accounts" :fields="accFields">
          <template slot="flow" slot-scope="data">
            {{$formatFlow(data.value)}}
          </template>
          <template slot="flowStatus" slot-scope="data">
            <div v-if="data.item.totalFlow === 0">
              {{$formatFlow(data.item.usedFlow, 'GB')}}/{{$formatFlow(data.item.totalFlow, 'GB')}}
            </div>
            <div v-if="data.item.totalFlow > 0">
              <b-progress
                animated :max="$convertFlow(data.item.totalFlow, 'GB')" 
                show-value :precision="1">
                <b-progress-bar :value="$convertFlow(data.item.usedFlow, 'GB')" variant="warning"></b-progress-bar>
                <b-progress-bar :value="$convertFlow(data.item.totalFlow, 'GB') - $convertFlow(data.item.usedFlow, 'GB')" variant="success"></b-progress-bar>
              </b-progress>
            </div>
            <!-- {{$formatFlow(data.item.usedFlow)}}/{{$formatFlow(data.item.totalFlow)}} -->
          </template>
          <template slot="expire" slot-scope="data">
            {{ $formatTime(data.value) }}
          </template>
          <template slot="detail" slot-scope="data">
            <b-button variant="primary" @click="viewAccDetail(data.item.id)">详情</b-button>
          </template>
        </b-table>
      </div>
    </b-tab>
    <b-tab title="网站用户">
      <user-overview :users="users" @actionClicked="viewUserDetail($event)" />
    </b-tab>
  </b-tabs>
</b-card>

</template>

<script>
import {getAllAccount, getAllUser} from '@/apis/admin.js'
import UserOverview from '@/components/admin/UserOverview'

export default {
  name: 'adminAccount',
  components: {
    UserOverview
  },
  data() {
    return {
      accounts: [],
      accFields: [
        {key: "id", label: "SS 账户ID"},
        {key: "userId", label: "网站ID"},
        {key: "port", label: "端口号"},
        {key: "flowStatus", label: "流量"},
        {key: "expire", label: "过期时间"},
        {key: "status", label: "状态"},
        {key: "detail", label: "详情"},
      ],
      users: []
    }
  },
  methods: {
    viewAccDetail(id) {
      this.$router.push({name: 'accountDetail', params: {id: id}})
    },
    viewUserDetail(id) {
      this.$router.push({ name: 'userDetail', path: "/user", params: {id: id} });
    }
  },
  created() {
    getAllAccount().then( resp => {
      this.accounts = resp.accounts;
    });
    getAllUser().then( resp => {
      // console.log( resp )
      this.users = resp.users
    })
  }
}
</script>
