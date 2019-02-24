<template>
<div>
  <b-card> 
    <!-- <order-overview-item :item="it" /> -->
    <div slot="header">
      <h5 class="my-0 font-weight-normal">套餐：{{item.id}}</h5>
    </div>
    <div class="text-center">
      <h1 class="card-title pricing-card-title">￥{{  item.price }}</h1>
      <ul class="list-unstyled mt-3 mb-4">
        <li><span class="h3">时长：{{ $formatTimeFromSeconds(item.duration) }}</span></li>
        <li><span class="h3">流量：{{ $formatFlow(item.flow, 'MB') }}</span></li>
        <!-- <li><span >{{ 'Buffer Period: ' }} {{ $formatTimeFromSeconds(item.bufferPeriod) }}</span></li> -->
      </ul>
    </div>
    <div slot="footer">
      <b-form-group label="支付方式">
        <b-row>
          <b-button :variant="alipay" class="bg-transparent offset-1 col-10 col-sm-4" v-if="item.alipay" @click="payment='alipay'">
            <img :src="require(`@/assets/alipay@2x.png`)" class="payment-image" alt="">
          </b-button>
          <b-button :variant="wechatpay" class="bg-transparent offset-1 col-10 offset-sm-2 col-sm-4" v-if="item.wechatpay" @click="payment='wechatpay'">
            <img :src="require(`@/assets/weixinpay@2x.png`)" class="payment-image" alt="">
          </b-button>
        </b-row>
      </b-form-group>
      <b-button type="button" class="btn-lg btn-block" 
        variant="primary" @click="$emit('choosed', {id: item.id, payment})" >选择</b-button>
    </div>
  </b-card>
</div>
</template>

<script>
export default {
  name: 'productItem',
  props: {
    item: Object,
  },
  data() {
    return {
      payment: 'alipay'
    }
  },
  computed: {
    alipay() {
      if(this.payment === 'alipay') {
        return 'primary';
      }
      return 'secondary';
    },
    wechatpay() {
      if(this.payment === 'wechatpay') {
        return 'primary';
      }
      return 'secondary';
    },
  }
}
</script>

<style>
.payment-image {
  width: 100%;
}
</style>
