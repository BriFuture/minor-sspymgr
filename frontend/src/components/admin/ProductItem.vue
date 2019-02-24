<template>
<div>
  <b-card>
    <div slot="header">
      <div class="row">
        <div class="col-4 col-sm-3">
          Id: {{ product.id }}
        </div>
        <div class="col-4 col-sm-3">
          启用：<a-switch v-model="product.enable"></a-switch>
        </div>
        <div class="col-4 col-sm-3">
          <b-button :variant="pVariant" :disabled="pVariant === 'secondary'"
            @click="$emit('productChange', product)">更改
          </b-button>
        </div>
      </div>
    </div>

    <b-form-group>
      <div class="row my-2">
        <b-input-group class="col-6 col-sm-3 mb-2" prepend="流量" append="GB">
          <b-form-input @change="flowChanged($event)" :value="product.flow" type="number"></b-form-input>
        </b-input-group>
        <b-input-group class="col-6 col-sm-3 mb-2" prepend="价格" append="元">
          <b-form-input @change="priceChanged($event)" :value="product.price" type="number"></b-form-input>
        </b-input-group>
        <b-input-group class="col-6 col-sm-3 mb-2" prepend="时长" append="天">
          <b-form-input @change="durationChanged($event)" :value="product.duration" type="number"></b-form-input>
        </b-input-group>
        <b-input-group class="col-6 col-sm-3 mb-2" prepend="缓冲期" append="时">
          <b-form-input @change="bufferChanged($event)" :value="product.bufferPeriod" type="number"></b-form-input>
        </b-input-group>
      </div>
      <slot name="qrcode">
      </slot>
    </b-form-group>
  </b-card>
  <b-modal title="">
  </b-modal>
</div>
</template>

<script>

export default {
  name: 'productItem',
  props: {
    product: Object,
  },
  data() {
    return {
      pVariant: 'secondary',
    }
  },
  methods: {
    flowChanged(value) {
      this.product.flow = value;
      this.pVariant = 'primary';
    },
    priceChanged(value) {
      this.product.price = value;
      this.pVariant = 'primary';
    },
    durationChanged(value) {
      this.product.duration = value;
      this.pVariant = 'primary';
    },
    bufferChanged(value) {
      this.product.bufferPeriod = value;
      this.pVariant = 'primary';
    }
  }
}
</script>

