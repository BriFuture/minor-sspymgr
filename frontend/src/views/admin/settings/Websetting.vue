<template>
  <div class="table-responsive">
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Key</th>
          <th scope="col">Value</th>
          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in settings" :key="s.id">
          <td>{{ s.id }}</td>
          <td>{{ s.key }}</td>
          <template v-if="s.type === 'Image'">
            <td >
              <span class="btn p-0" v-if="s.value">
                <img :src="'data:image/png;base64, ' + s.value" width="32" height="32"/>
              </span>
            </td>
            <td>
              <button class="btn btn-sm btn-primary" type="button">{{ 'update' }}</button>
            </td>
          </template>
          <template v-else-if="s.type === 'Boolean'">
            <td>
              <a-switch :checked="s.value === '1'" @change="switchSetting(s)" />
            </td>
            <td ><label></label></td>
          </template>
          <template v-else-if="s.type == 'Number'" >
            <td >
              <input type="number" :value="s.value"></td>
            <td>
              <label ></label>
            </td>
          </template>
          <template v-else >
            <td >{{ s.value }}</td>
            <td>
              <button class="btn btn-sm btn-primary" type="button"
                >{{ 'update' }}</button>
            </td>
          </template>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import {getAllSettings} from '@/apis/admin.js'

export default {
  name: 'adminWebSetting',
  data() {
    return {
      settings: [],
    }
  },
  methods: {
    switchSetting(s) {
      if( s.value === '1') {
        s.value = '0';
      } else {
        s.value = '1';
      }
    }
  },
  created() {
    getAllSettings().then( resp => {
      console.log(resp);
      this.settings = resp.setting;
    })
  }
}
</script>

<style>

</style>
