<template>
  <div>
    <b-card>
      <b-button variant="primary" @click="newAnnouncement = true">
        新公告
      </b-button>
      <div class="text-lg" v-if="announcements.length === 0">暂无公告</div>
    </b-card>

    <b-table responsive :items="announcements" :fields="fields">
      <template slot="action" slot-scope="row">
        <b-button variant="success" class="ml-2" @click="modify(row.item.id)"
          >修改</b-button>
        <b-button class="ml-2" @click="del(row.item.id, row.index)"
          >删除</b-button>
      </template>
      <template slot="content" slot-scope="data">
        <!-- <div v-html="data.value"></div> -->
        <b-form-textarea max-rows="3" readonly :value="data.value">

        </b-form-textarea>
      </template>
    </b-table>
    <b-modal title="创建新公告" v-model="newAnnouncement"
      size="lg">
      <create-announcement @submitted="newAnnouncementCreated()" />
      <div slot="modal-footer"></div>
    </b-modal>
  </div>
</template>

<script>
import AnnouncementArea from '@/components/user/Announcement'
import CreateAnnouncement from '@/components/admin/CreateAnnouncement'
import {getAnnouncements, delAnnouncement} from '@/apis/admin'

export default {
  name: "adminAnnouncement",
  components: {
    AnnouncementArea,
    CreateAnnouncement
  },
  data() {
    return {
      announcements: [],
      fields: [
        {key: "id"},
        {key: "title"},
        {key: "variant"},
        {key: "top"},
        {key: "content"},
        {key: 'createTime', formatter: this.$formatTime},
        {key: "action", label: "Action"},
      ],
      newAnnouncement: false
    }
  },
  created() {
    this.refresh()
  },
  methods: {
    modify(id) {
      console.log("TODO", id)
    },
    del(id, index) {
      delAnnouncement({id}).then( resp => {
        console.log(resp)
      })
      let ann = null;
      this.announcements.splice(index, 1)

    },
    refresh() {
    getAnnouncements().then( resp => {
      this.announcements = resp.announcements;
    })
    },
    newAnnouncementCreated() {
      this.refresh()
      this.newAnnouncement = false
    }
  }
}
</script>

<style>

</style>
