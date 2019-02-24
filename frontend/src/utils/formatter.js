import moment from 'moment'

moment.locale('zh-cn')

// const KB = 1024
const MB = 1024 * 1024
const GB = 1024 * 1024 * 1024
/**
 * 将字节表示的流量转换成可读的字符串
 * @param {Number} bytes 
 */
export function formatFlow(flow, unit) {
    let u = 1;
    if( unit === 'GB' ) {
        u = GB;
    } else if( unit === 'MB' ) {
        u = MB;
    } else if(unit === 'KB') {
        u = 1024;
    }
    flow *= u;
    if( flow > GB ) {
        let g = flow / GB;
        return g.toFixed(1) + 'Gb';
    } else if ( flow > MB ) {
        let m = flow / MB;
        return m.toFixed(1)+ 'Mb';
    } else {
        let k = flow / 1024;
        return k.toFixed(0) + 'Kb';
    }
}

/**
 * 将流量转换为不同单位计量的数字
 * @param {Number} flow unit in bytes
 * @param {String} toUnit MB, GB
 * @param {*} unit 
 */
export function convertFlow(flow, toUnit, unit) {
    if( !unit ) {
        unit = 1
    }
    flow *= unit;
    if(toUnit === 'GB') {
        return flow / GB;
    } else if( toUnit === 'MB') {
        return flow / MB;
    }
    return flow;
}

/**
 * 
 * @param {Number} timestapm 以s为单位的时间戳
 */
export function formatTime(timestamp) {
    if( !timestamp ) {
        return '';
    }
    let ts = parseFloat(timestamp) * 1000
    // let now = new Date(ts)
    return moment(ts).format("YYYY-MM-DD, h:mm");
}
// const MINUTE = 60
// const HOUR = 3600
// const DAY = 24 * 3600
export function formatTimeFromSeconds(seconds) {
    // let day, hour;
    // if( seconds > DAY ) {
    //     day = Math.floor(seconds / DAY)
    // } else if( seconds > HOUR ) {
    //     hour = Math.floor(seconds / HOUR)
    // }
    return moment.duration({seconds: seconds}).humanize()
}
