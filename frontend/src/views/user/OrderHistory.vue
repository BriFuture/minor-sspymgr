<template>
<div>
  <loading-modal v-model="loading" />
  <div v-if="orders.length === 0 && !loading" class="text-center h3 text-danger">
    没有找到记录
  </div>
  <b-table responsive striped hover :items="orders" :fields="fields">
    <template slot="bufferPeriodExpire" slot-scope="data">
      {{$formatTime(data.value)}}
    </template>
    <template slot="expire" slot-scope="data">
      {{$formatTime(data.value)}}
    </template>
    <template slot="orderTime" slot-scope="data">
      {{$formatTime(data.value)}}
    </template>
  </b-table>
</div>
</template>

<script>
import LoadingModal from '@/components/LoadingModal.vue'
import {getOrderHistory} from '@/apis/user'

export default {
  name: 'userOrderHistory',
  components: {
    LoadingModal,
  },
  data() {
    return {
      orders: [],
      fields: [
        'id',
        {key: 'pid', label: '订单类型'},
        {key: 'bufferPeriodExpire', label: '缓冲期'},
        {key: 'expire', label: '到期时间'},
        {key: 'orderTime', label: '订单生效时间'},
      ],
      loading: true
    }
  },
  created() {
    getOrderHistory().then( resp => {
      this.loading = false;
      console.log(resp)
      this.orders = resp
    })
  }
}
</script>
