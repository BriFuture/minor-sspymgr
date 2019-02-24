<template>
  <b-card :title="category" >
    <div class="text-center" v-b-tooltip.hover title="点击选择新的二维码">
      <img class="border" @click="showFile = !showFile" 
        :src="'data:image/png;base64, ' + image" 
        style="min-height:150px; min-width:150px; max-height:300px; max-width:300px;" />
    </div>
    <b-collapse v-model="showFile" id="qrcodeImageUploader">
      <div class="my-2">
        <b-form-file :value="file" :state="Boolean(file)" @change="fileChanged($event)"
          placeholder="更换二维码"></b-form-file>
        <div class="mt-3">
          <span >Selected file: {{file && file.name}}</span>
          <span class="float-right">
          </span>
        </div>
      </div>
    </b-collapse>
    <div slot="footer">
      <b-form-group class="mb-2">
        <b-input-group prepend="描述" v-b-tooltip.hover title="便于管理员区分不同的二维码">
          <b-form-input @change="updated=true" v-model="qrcode.desc"></b-form-input>
        </b-input-group>
        <b-input-group prepend="标记" v-b-tooltip.hover title="保留的字段">
          <b-form-input @change="updated=true" v-model="qrcode.remark"></b-form-input>
        </b-input-group>
        <b-input-group prepend="路径" v-b-tooltip.hover title="保存在服务器上的路径">
          <b-form-input @change="updated=true" v-model="qrcode.path"></b-form-input>
        </b-input-group>
      </b-form-group>
      <div>
        <b-button variant="primary" @click="$emit('update', qrcode)" 
          :disabled="!updated">上传</b-button>
        <b-button class="float-right" @click="$emit('delete', qrcode)" 
          >删除</b-button>
      </div>
    </div>
  </b-card>
</template>

<script>

var fileTypes = [
  'image/jpeg',
  'image/pjpeg',
  'image/jpg',
  'image/png',
  'image/gif',
]

function validFileType(file) {
  for(let i = 0; i < fileTypes.length; i++) {
    if(file.type === fileTypes[i]) {
      return true;
    }
  }
  return false;
}

export default {
  name: 'productQrcode',
  props: {
    qrcode: Object,
    category: String,
  },
  data() {
    return {
      file: null,
      showFile: false,
      image: null,
      updated: false,
      // imgSrc: null,
    }
  },
  watch: {
    qrcode(nv, ov) {
      if( this.qrcode.qrcode) {
        this.image = this.qrcode.qrcode;
      }
    },
  },
  created() {
    // if(!this.qrcode.qrcode) {
    //   this.qrcode.qrcode = 'R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
    // }
    if( this.qrcode.qrcode) {
      this.image = this.qrcode.qrcode;
    }
  },
  methods: {

    fileChanged(event) {
      let file = event.target.files[0];
      this.file = file;
      if(validFileType(file)) {
        // this.imgSrc = window.URL.createObjectURL(file);
        const reader = new FileReader();
        reader.readAsBinaryString(file);
        reader.onload = (e) => {
          this.image = btoa(e.target.result);
          this.qrcode.qrcode = this.image;
          this.updated = true;
        }
      } else {
        this.file = null
        alert('File name ' + file.name + ': Not a valid file type. Update your selection.');
      }
    }
  }
}
</script>

<style>

</style>
