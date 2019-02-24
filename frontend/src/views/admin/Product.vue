<template>
  
<div class="table-responsive">
  <b-card class="my-2">
    <b-button variant="primary" data-toggle="modal" data-target="#new_product">
      {{ 'Add New Product' }}
    </b-button>
  </b-card>
  
  <b-table striped hoverd :items="products" :fields="fields">
    <template slot="flow" slot-scope="data">
      {{$formatFlow(data.value, "MB")}}
    </template>
    <template slot="price" slot-scope="data">
      ￥{{data.value}}
    </template>
    <template slot="action" slot-scope="row">
      <b-button variant="primary" @click="viewDetail(row.index)">操作</b-button>
    </template>
    <template slot="enable" slot-scope="data">
      <a-switch :checked="data.value === true" :disabled="true"></a-switch>
    </template>
  </b-table>
</div>

</template>>

<script>
import {getAllProducts} from '@/apis/admin.js'
import ProductItem from '@/components/ProductItem.vue'

export default {
  name: "products",
  data() {
    return {
      products: [],
      fields: [
        { key: 'id', label: "Product ID" },
        { key: 'flow', label: "流量" },
        { key: 'price', label: "价格" },
        { key: 'duration', label: "时长", formatter: this.$formatTimeFromSeconds },
        { key: 'bufferPeriod', label: "缓冲期", formatter: this.$formatTimeFromSeconds },
        { key: 'enable', label: "是否启用" },
        { key: 'action', label: "操作" },
      ]
    };
  },
  methods: {
    init() {
      getAllProducts().then( resp => {
        console.log( resp )
        this.products = resp.products;
      });
    },
    viewDetail(index) {
      this.$router.push( {name: 'productDetail', params: {id: index+1} })
    }
  },
  created() {
    this.init();
  }
}
</script>
