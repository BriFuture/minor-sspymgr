<template>
<div class="form-group">
  <span class="mr-3">
    <i :class="inputProp.icon"></i>
  </span>
  <label class="form-label">{{ inputProp.title }}</label>
  <input class="form-control" 
    :type="inputType" 
    :placeholder="inputProp.placeholder"
    :value="value"
    :readonly="readonly"
    @input="$emit('valueChanged', $event.target.value)" >
</div>
</template>

<script>
export default {
  name: 'textInput',
  props: {
    inputProp: {},
    value: '',
    inputType: {
      type: String,
      default: 'text'
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },
  model: {
    prop: 'value',
    event: 'valueChanged'
  }
}
</script>

