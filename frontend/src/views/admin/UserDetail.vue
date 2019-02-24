<template>
<div>
  <div class="my-2">
    <b-button variant="primary" @click="$router.go(-1)">
      {{ '返回' }}
    </b-button>
  </div>
  <b-card >
  <user-item :user="user" />
  </b-card>
  <div>
    <account-item :account="account" :accFlow="accountFlow" />
  </div>
</div>
</template>

<script>
import {getUserDetail} from '@/apis/admin'
import AccountItem from '@/components/admin/AccountItem.vue'
import UserItem from '@/components/admin/UserItem.vue'

export default {
  name: 'userDetail',
  components: {
    AccountItem,
    UserItem
  },
  data() {
    return {
      user: {},
      userType: null,
      account: {},
      accountFlow: {}
    }
  },
  created() {
    getUserDetail({
      userId: this.$route.params.id
    }).then( resp => {
      console.log(resp)
      if(resp.status === "success") {
        this.user = resp.user;
        this.userType = this.user.type;
        this.account = resp.account;
        this.accountFlow = resp.accountFlow;
      }
    })
  }
}
</script>
