import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import '@/assets/common.css'
import Vue from 'vue';
import UtilsPlugin from '@/utils/utilsPlugin'
Vue.use(UtilsPlugin);
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)

Vue.config.productionTip = false;

import 'ant-design-vue/dist/antd.css';
import Antd from 'ant-design-vue'

Vue.use(Antd)

import VeHistogram from 'v-charts/lib/histogram.common'
Vue.component(VeHistogram.name, VeHistogram)