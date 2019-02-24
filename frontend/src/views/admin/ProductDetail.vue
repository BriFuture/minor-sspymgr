<template>
<div>
  <b-card>
    <div slot="header">
      <div class="row">
        <div class="col-4 col-sm-3">
          Id: {{ product.id }}
        </div>
        <div class="col-4 col-sm-3">
          启用：<a-switch v-model="product.enable" @change="pVariant = 'primary'"></a-switch>
        </div>
        <div class="col-4 col-sm-3">
          <b-button :variant="pVariant" :disabled="pVariant === 'secondary'"
            @click="productChange()">更改
          </b-button>
        </div>
      </div>
    </div>

    <b-form-group>
      <div class="row my-2">
        <b-input-group class="col-6 col-sm-3 mb-2" prepend="流量" append="GB">
          <b-form-input @change="flowChanged($event)" 
            :value="flow" type="number"></b-form-input>
        </b-input-group>
        <b-input-group class="col-6 col-sm-3 mb-2" prepend="价格" append="元">
          <b-form-input @change="pVariant = 'primary'" v-model="product.price" type="number"></b-form-input>
        </b-input-group>
        <b-input-group class="col-6 col-sm-3 mb-2" prepend="时长" append="天">
          <b-form-input @change="durationChanged($event)"  
            :value="duration" type="number"></b-form-input>
        </b-input-group>
        <b-input-group class="col-6 col-sm-3 mb-2" prepend="缓冲期" append="时">
          <b-form-input @change="bufferChanged($event)" 
            :value="bufferPeriod" type="number"></b-form-input>
        </b-input-group>
      </div>
      <div class="row">
        <div class="mt-2 col-12 col-sm-6">
          <product-qrcode :qrcode="alipay" category="alipay" 
            @update="updateQrcode($event)" @delete="deleteQrcode($event)" />
        </div>
        <div class="mt-2 col-12 col-sm-6">
          <product-qrcode :qrcode="wechatpay" category="wechatpay" 
            @update="updateQrcode($event)" @delete="deleteQrcode($event)" />
        </div>
      </div>
    </b-form-group>
  </b-card>
</div>
</template>

<script>
import ProductQrcode from '@/components/admin/ProductQrcode'
import {getProduct, updateProduct, updateProductQrcode, deleteProductQrcode} from '@/apis/admin'

export default {
  name: 'productDetail',
  components: {
    ProductQrcode
  },
  data() {
    return {
      product: {
        'flow': 10,
        'price': 4,
        'duration': 30,
        'bufferPeriod': 20,
      },
      alipay: {
        pid: -1,
        category: 'alipay',
        desc: '',
        qrcode: 'R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
      },
      wechatpay: {
        pid: -1,
        category: 'wechatpay',
        desc: '',
        qrcode: 'R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
      },
      pVariant: 'secondary',
      durationUnit: "月"
    }
  },
  computed: {
    bufferPeriod() {
      return this.product.bufferPeriod / 3600;
    },
    duration() {
      return this.product.duration / 3600 / 24;;
    },
    flow() {
      return this.product.flow / 1024;
    }
  },
  methods: {
    updateQrcode(qrcode) {
      let param = {
        ...qrcode,
        productId: this.product.id,
      }
      updateProductQrcode(param).then( resp => {
        // console.log(resp)
        if(resp.status === 'success'){
          location.reload();
        } else {
          alert('Something Wrong')
        }
      });
    },
    deleteQrcode(qrcode) {
      let param = {
        id: qrcode.id
      }
      deleteProductQrcode(param).then( resp => {
        // console.log(resp)
        if(resp.status === 'success'){
          location.reload();
        } else {
          alert('Something Wrong')
        }
      });
    },
    flowChanged(value) {
      this.pVariant = 'primary';
      this.product.flow = value * 1024;
    },
    bufferChanged(value) {
      this.pVariant = 'primary';
      this.product.bufferPeriod = value * 3600;
    },
    durationChanged(value) {
      this.pVariant = 'primary';
      this.product.duration = value * 3600;
    },
    productChange() {
      updateProduct({
        ...this.product,
      }).then( resp => {
        this.pVariant = 'secondary'
      })
    }
  },
  created() {
    getProduct({id: this.$route.params.id}).then(resp => {
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
      }
    })
  }
}
</script>

