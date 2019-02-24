<template>
<div>
  <b-card title="公告" class="my-2">
    <announcement-area class="my-2 px-1 py-1" v-for="ann in announcements" :key="ann.id" 
      :title="ann.title" :content="ann.content" />
  </b-card>
  
  <b-card class="px-1 py-1">
    <b-button variant="primary" class="text-lg" 
      @click="$router.push({path: '/account'})">账户详细信息</b-button>
    <div class="row py-2">
      <div class="col-12 col-sm-4 text-left text-md">
        <text-input :input-prop="{'title': 'Host', 'icon': 'fas fa-network-wired'}"
          :readonly="true"
          v-model="ad.server" />
      </div>
      <div class="col-12 col-sm-4 text-left text-md">
      <text-input :input-prop="{'title': 'Port', 'icon': 'fas fa-ethernet'}"
        :readonly="true"
        v-model="ad.port" />
      </div>
      <div class="col-12 col-sm-4 text-left text-md">
        <text-input :input-prop="{'title': 'Password', 'icon': 'fas fa-key'}" 
          v-model="ad.password" 
          :readonly="true" />
      </div>
    </div>
  </b-card>

  <b-card title="流量日统计" class="mt-2">
    <day-flow-usage ref="flowUsage" @selectDate="changeFlowDate($event)" />
  </b-card>
</div>
</template>

<script>
import {getUserAccount, getDayFlowUsage, 
  getMonFlowUsage, getAnnouncements} from '@/apis/user.js'

import TextInput from '@/components/TextInput.vue'
import DayFlowUsage from '@/components/DayFlowUsage'
import AnnouncementArea from '@/components/user/Announcement.vue';

export default {
  name: 'userIndex',
  components: {
    TextInput,
    DayFlowUsage,
    AnnouncementArea
  },
  data() {
    return {
      ad: {},
      announcements: []
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
    getUserAccount().then( resp => {
      this.ad = resp.account;
    });
    this.changeFlowDate(this.$moment());
    getAnnouncements().then( resp => {
      console.log(resp)
      this.announcements = resp.announcements;
    })
  }
}
</script>
