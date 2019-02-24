<template>
  <b-card title="公告设置" :border-variant="variant" >
    <b-form-group>
      <b-input-group prepend="标题" for="announce-title">
        <b-form-input id="announce-title" v-model="title"></b-form-input>
      </b-input-group>
    </b-form-group>
    <b-form-group>
      <b-row>
        <div class="col-6 col-sm-4">
          <label>Variant</label>
          <b-form-select v-model="variant"
            @toggle="changeVaraint()" :options="variantOptions">
          </b-form-select>
        </div>
        <div class="col-6 col-sm-4">
          <label>Level</label>
          <b-form-input type="number" v-model="level"></b-form-input>
        </div>
      </b-row>
    </b-form-group>
    <b-form-group>
      <b-form-textarea :rows="10" v-model="content">
      </b-form-textarea>
    </b-form-group>
    <b-button :variant="state" :disabled="state === 'secondary'"
      @click="submit()">提交</b-button>
  </b-card>
</template>

<script>
import {createAnnouncement} from '@/apis/admin.js'

export default {
  name: 'createAnnouncement',
  data() {
    return {
      title: '',
      level: 0,
      content: "",
      variant: 'success',
      variantOptions: [
        {value: 'success', text: "success"},
        {value: 'primary', text: "primary"},
        {value: 'warning', text: "warning"},
        {value: 'danger', text: "danger"},
      ]
    }
  },
  computed: {
    state() {
      return this.title.length === 0 ? 'secondary' : 'primary'; 
    }
  },
  methods: {
    submit() {
      createAnnouncement({ 
        title: this.title, 
        variant: this.variant,
        level: this.level,
        content: this.content
      }).then( resp => {
        console.log(resp)
        this.resetAll()
        this.$emit("submitted");
      })
    },
    resetAll() {
        this.title="";
        this.variant = 'success';
        this.content = "";
        this.level = 0;

    }
  }
}
</script>
