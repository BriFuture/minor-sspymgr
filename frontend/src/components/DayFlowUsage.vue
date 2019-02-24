<template>
<div>
  <b-row class="my-2">
    <div class="col-10 col-sm-5 row">
      <label class="col-8 text-lg">流量单位:</label>
      <b-select class="col-4" :value="flowUnit" :options="unitOptions" @change="changeUnit($event)">
      </b-select>
    </div>
    <div class="col-12 col-sm-5 offset-sm-2">
      <b-button class="mx-3" @click="$emit('selectDate', date.subtract(1, 'day'))">前一天</b-button>
      <a-date-picker @change="onDateChange" :allowClear="false"  v-model="date" />
    </div>
  </b-row>
  <ve-histogram :data="chartData" :settings="chartSettings" :extend="extend" />
</div>
</template>

<script>
const KB = 1024;
const MB = 1024 * 1024;
const GB = 1024 * 1024 * 1024;
export default {
  name: 'accountDetail',
  data() {
    this.chartSettings = {
        metrics: ['flow'],
        dimension: ['hour']
    };
    this.extend = {
      series: {
        label: { show: true, position: "top", formatter: this.formatFlow }
      }
    }
    return {
      chartData: {
        columns: ['hour', 'flow'],
        rows: []
      },
      flowUnit: 1,
      flowUnitText: 'B',
      unitOptions: [
        {value: MB, text: "MB"},
        {value: GB, text: "GB"},
        {value: KB, text: "KB"},
        {value: 1,  text: "B"},
      ],
      date: null
    }
  },
  computed : {
    dateString() {
      if(this.date === null)
        return ''
      return this.date.format("YYYY-MM-DD")
    }
  },
  methods: {
    setRecords(records) {
      let dr;
      for(let dr of this.chartData.rows) {
        dr.flow = 0 ;
      }
      let max = 0;
      for(let r of records) {
        dr = this.chartData.rows[r.hour];
        dr.flow += r.flow ;
        if(dr.flow > max) {
          max = dr.flow
        }
      }
      this.flowUnit = 1;
      if( max > GB ) {
        // this.flowUnit = MB;
        this.changeUnit(GB);
      } else if( max > MB ) {
        this.changeUnit(MB);
      } else if( max > KB ) {
        this.changeUnit(KB);
      } else {
        this.changeUnit(1);
      }
    },
    onDateChange(date) {
      this.$emit('selectDate', date)
    },
    setDate(timestamp) {
      this.date = this.$moment(timestamp);
    },
    changeUnit(unit) {
      let r;
      let rate = this.flowUnit / unit;
      this.flowUnit = unit;
      for(let o of this.unitOptions) {
        if(o.value == this.flowUnit) {
          this.flowUnitText = o.text.substring(0, 1);
          break;
        }
      }
      for(let i = 0; i < 24; i++){
        r = this.chartData.rows[i];
        r.flow = r.flow * rate;
      } 
    },
    formatFlow(params) {
      return (params.value.toFixed(2)) + this.flowUnitText;
    }
  },
  created() {
    for(let i = 0; i < 24; i++) {
      this.chartData.rows.push({'hour': i, 'flow': 0})
    }
  }
}
</script>
