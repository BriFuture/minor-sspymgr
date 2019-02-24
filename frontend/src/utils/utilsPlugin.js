import {formatFlow, formatTime, formatTimeFromSeconds,
    convertFlow} from './formatter'
import moment from 'moment'
export default {
    install(Vue, options) {
        Vue.prototype.$formatFlow = formatFlow;
        Vue.prototype.$formatTime = formatTime;
        Vue.prototype.$formatTimeFromSeconds = formatTimeFromSeconds;
        Vue.prototype.$convertFlow = convertFlow;
        Vue.prototype.$moment = moment;
    }
}