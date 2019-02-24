<template>
<div>
  <loading-modal v-model="loading" />
  <div v-if="products.length === 0 && !loading" class="text-center h3 text-danger">
    没有找到记录
  </div>
  <b-row class="mx-0">
    <template v-for="item in products" >
      <product-item class="col-12 col-sm-6" :key="item.id" 
        :item="item"  @choosed="viewDetail($event)"> 
      </product-item>
    </template>
  </b-row>
  <b-modal title="提示" v-model="unableHint">
    <b-alert variant="success" show>现在无法购买</b-alert>
    <div v-for="(t, index) in unableHintText" :key="index" class="text-lg">{{t}}</div>
  </b-modal>
</div>
</template>

<script>
import {getAvailableProducts, canPlaceOrder} from '@/apis/user'
import LoadingModal from '@/components/LoadingModal.vue'
import ProductItem from '@/components/ProductItem.vue'

export default {
  name: 'userProduct',
  components: {
    LoadingModal,
    ProductItem
  },
  data() {
    return {
      products: [],
      loading: true,
      unableHint: false,
      unableHintText: []
    }
  },
  created() {
    getAvailableProducts().then( resp => {
      this.products = resp;
      this.loading = false;
    })
  },
  methods: {
    viewDetail(detail) {
      console.log(detail)
      let id = detail.id;
      let payment = detail.payment;
      // console.log(id)
      this.unableHintText = []
      canPlaceOrder().then( resp => {
        // console.log(resp)
        if( resp.canPlaceOrder === true ) {
          this.$router.push({name: 'productDetail', path:'/product', params: {id, payment}})
        } else {
          this.unableHint = true;
          this.unableHintText.push(`你的账户将在 ${resp.expire} 过期`)
          this.unableHintText.push(`你可以在 ${resp.nextPlaceOrderTime} 之后购买流量`)
        }
      })
    }
  }
}
</script>

