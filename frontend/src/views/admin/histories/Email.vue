<template>
<div>
  <b-table responsive striped hover :items="emails" :fields="fields">
    <template slot="time" slot-scope="data" >
      {{$formatTime(data.value)}}
    </template>
  </b-table>
  <b-pagination align="center" size="md" :limit="10" 
    :total-rows="totalItems" v-model="currentPage" 
    :per-page="itemsPerPage" @change="refresh($event)" >
  </b-pagination>
</div>
</template>

<script>
import {getAllEmails, getEmailHistory} from '@/apis/admin'

export default {
  name: 'adminEmail',
  data() {
    return {
      emails: [],
      fields: [
        {key: "id", sortable: true},
        {key: "to", sortable: true},
        {key: "subject"},
        {key: "remark"},
        {key: "type"},
        {key: "content"},
        {key: 'time'},
        {key: "action", label: "Action"},
      ],
      currentPage: 1,
      itemsPerPage: 20,
      totalItems: 0
    }
  },
  methods: {
    refresh(page) {
      if(page === undefined) {
        page = this.currentPage;
      }
      getEmailHistory({
        page: page,
        perPage: this.itemsPerPage        
      }).then( resp => {
        console.log(resp)
        this.totalItems = resp.emails.total;
        this.emails = resp.emails.items;
      });
    }
  },
  created() {
    this.refresh()
  }
}
</script>
