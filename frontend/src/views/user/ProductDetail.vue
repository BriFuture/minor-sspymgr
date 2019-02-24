<template>
<div>
  <loading-modal v-model="loading" />
  <div class="text-primary text-center row mx-0">
    <div class="col-6 col-sm-3">
      <b-button @click="$router.push({path: '/product'})">选择其他方案</b-button>
    </div>
    <div class="col-6 col-sm-3 h3">价格：￥{{ price }}</div>
    <div class="col-6 col-sm-3 h3">流量：{{ $formatFlow(product.flow, 'MB') }}</div>
    <div class="col-6 col-sm-3 h3">{{ '时长：' }} {{ $formatTimeFromSeconds(product.duration) }}</div>
  </div>
  <hr />
  <b-card v-if="alipay">
    <div>
      <div class="text-center" id="alipay_qrcode">
        <p>扫一扫付款（元）</p>
        <p class="h3 text-danger font-weight-bold">{{price}}</p>
        <div style="width: 220px;" class="mx-auto card py-1">
          <img style="vertical-align: top" 
            :src="'data:image/png;base64, ' + alipay.qrcode" 
            class="d-block qrcode-img-fixed mx-auto" alt="二维码已过期"/>
          <div style="height:42px;">
            <img src="https://t.alipayobjects.com/images/T1bdtfXfdiXXXXXXXX.png"
              alt="扫一扫标识" class="pb-4">
            <div class="d-inline-block">
              打开手机支付宝<br>扫一扫继续付款
            </div>
          </div>
          <div class="timeout" :class="{'d-none': (remainSeconds > 0)}">二维码已过期</div>
        </div>
        <a style="color: #a6a6a6;" href="https://mobile.alipay.com/index.htm" target="_blank">
          首次使用请下载手机支付宝</a>
        <div v-show="remainSeconds>0">请于 {{ remainSecondsText }} 内支付</div>
      </div>
    </div>
  </b-card>
  <b-card v-if="wechatpay">
    <div class="d-block mx-3">
      <h3 class="d-block text-center">{{ 'Wechatpay' }}</h3>
      <img :src="'data:image/png;base64, ' + wechatpay.qrcode" class="d-block qrcode-img-fixed mx-auto"/>
    </div>
  </b-card>

  <div class="pt-2">
    <b-button variant="primary" type="button" class="float-right mr-4" 
      :disabled="!completed || (remainSeconds === 0)"
      @click="confirmOrder()">
      {{ confirmOrderText }}
    </b-button>
  </div>
  <b-modal title="完成订单" :no-close-on-backdrop="true" 
    :ok-only="true" v-model="orderHint" @ok="completeOrder()">
    <p>{{orderHintText}}</p>
  </b-modal>
</div>
</template>

<script>
import {getProductDetail, confirmOrder, canPlaceOrder} from '@/apis/user'
import { setTimeout, setInterval, clearInterval } from 'timers';
import LoadingModal from '@/components/LoadingModal.vue'

const WaitingSeconds = 20 * 1000;
export default {
  name: 'userProductDetail',
  components: {
    LoadingModal
  },
  data() {
    return {
      product: {},
      alipay: null,
      wechatpay: null,
      completed: false,
      orderHint: false,
      orderHintText: '',
      remainSeconds: 90,
      confirmOrderText: '确认支付',
      loading: true,
    }
  },
  computed: {
    pid() {
      return parseInt(this.$route.params.id)
    },
    price() {
      if(this.product.price)
        return this.product.price.toFixed(1)
      return 5
    },
    remainSecondsText() {
      if(this.remainSeconds > 60) {
        return '1 分钟'
      }
      return this.remainSeconds + ' 秒'
    }
  },
  created() {
    canPlaceOrder().then( resp => {
      if(resp.canPlaceOrder === false) {
        this.$router.go(-1);
      }
    })
    getProductDetail({ product: this.pid}).then( resp => {
      this.loading = false;
      if( resp.status === 'success') {
        this.product = resp.product;
        for(let qrcode of resp.qrcodes) {
          if( qrcode ) {
            if( qrcode.category === 'alipay') {
              this.alipay = qrcode;
            } else if ( qrcode.category === 'wechatpay') {
              this.wechatpay = qrcode;
            }
          }
        }
        let remainTimer = setInterval(() => {
          this.remainSeconds -= 1;
          if(this.remainSeconds == 0) {
            this.confirmOrderText = '二维码已失效'
            clearInterval(remainTimer)
          }
        }, 1000)
        setTimeout(() => {
          this.completed = true;
        }, WaitingSeconds);
      }
      else
        alert("Invalid Product")
    })
  },
  methods: {
    cancleOrder() {
      this.$route.go(-1)
    },
    confirmOrder() {
      // let resp = {'status': 'success'};
      confirmOrder({product: this.pid}).then( resp => {
        if( resp.status === 'success') {
          this.orderHintText = "完成订单，从现在起你可以使用翻墙服务 30 天。\
          点击下方的按钮，查看服务器、账户和密码";
        } else {
          this.orderHintText = "订单失败，请联系管理员";
        }
        this.orderHint = true;
        // console.log(resp)
      })
    },
    completeOrder() {
      this.$router.push({path: `/account`})
    }
  }
}
</script>

<style>
.qrcode-img-fixed {
  width: 180px;
  height: 180px;
  /* min-width: 220px;
  max-width: 260px;
  min-height: 220px;
  max-height: 260px; */
}
.timeout {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  background: rgba(255,255,255,.95);
  color: #222;
  line-height: 200px;
  text-align: center;
  z-index: 1;
}
</style>
