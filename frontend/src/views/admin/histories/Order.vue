<template>
  
<div class="table-responsive">
  <b-table responsive striped hover :items="orders" :fields="fields">
    <template slot="time" slot-scope="data" >
      {{$formatTime(data.value)}}
    </template>
    <template slot="user" slot-scope="data" >
      {{ data.item.uid }}
    </template>
    <template slot="pay" slot-scope="data" >
      <span v-if="data.item.alipay">{{ 'Alipay: ' + o.alipay }}</span>
      <span v-if="data.item.wechatpay">{{ 'WechatPay: ' + o.wechatpay }}</span>
    </template>
  </b-table>
  <b-pagination align="center" size="md" :limit="10" 
    :total-rows="totalOrders" v-model="currentPage" 
    :per-page="itemsPerPage" @change="refresh($event)" >
  </b-pagination>
</div>

</template>>

<script>
import {getOrderHistory} from '@/apis/admin.js'
export default {
  name: "adminOrder",
  data() {
    return {
      orders: [],
      fields: [
        {key: "id", sortable: true},
        {key: "pid", sortable: true},
        {key: "user", label: "user"},
        {key: "code"},
        {key: "pay", label: "支付方式"},
        {key: 'orderTime', formatter: this.$formatTime},
        {key: 'bufferPeriodExpire', formatter: this.$formatTime},
        {key: 'expire', formatter: this.$formatTime},
        {key: "action", label: "Action"},
      ],
      currentPage: 1,
      itemsPerPage: 20,
      totalOrders: 0
    }
  },
  computed: {
  },
  methods: {
    refresh(page) {
      if(page === undefined) {
        page = this.currentPage;
      }
      getOrderHistory({
        page: page,
        perPage: this.itemsPerPage
      }).then( resp => {
        this.totalOrders = resp.orders.total;
        this.orders = resp.orders.items;
      })
    }
  },
  created() {
    this.refresh()
  }
}
</script>