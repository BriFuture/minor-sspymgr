<template>
  <b-card class="rounded-0 text-left form-signin">
    <b-card-header>
      <h3 class="mb-0">{{ 'Please Sign in' }}</h3>
    </b-card-header>
    <div class="card-body">
      <form class="form needs-validation" role="form" autocomplete="off" method="post">
        <b-form-group :state="emailState">
          <label for="signinEmail" class="sr-only">{{ 'Email address' }}</label>
          <b-form-input type="email" id="signinEmail" name="email" 
            class="form-control"  required autofocus="" 
            v-model="email" :state="emailState"
          />
          <b-form-invalid-feedback>
            <div v-if="errors.email">{{ errors.email }}</div>
            <div v-else>{{ '请填写正确的邮箱' }}</div>
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group :state="passwordState">
          <label for="signinPassword" class="sr-only">{{ 'Password' }}</label>
          <b-form-input type="password" id="signinPassword" name="password" 
            class="form-control" required v-model="password" :state="passwordState" />
          <b-form-invalid-feedback>
            <div v-if="errors.password">{{ errors.password }}</div>
            <div v-else>{{ '请输入密码(至少 6 个字符)!' }}</div>
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group class="mb-1">
          <label>
            <b-form-checkbox type="checkbox" value="remember-me" name="keep_signedin" v-model="remember">
              {{ 'Remember me' }}
            </b-form-checkbox>
          </label>
        </b-form-group>
        <b-form-group>
          <span class=""><router-link to="/resetPassword">{{ 'Forget Password?' }}</router-link></span>
          <span class="float-right"><router-link to="/signup">{{ 'No Account?' }}</router-link></span>
        </b-form-group>
        <b-button variant="primary" class="btn-lg btn-block" type="button" @click="toSignIn()">
          {{ 'Sign in' }}
        </b-button>
        <p class="mt-5 mb-3 text-muted text-right">© 2017-2018</p>
      </form>
    </div>
    <!--/card-block-->
  </b-card>
</template>

<script>
import { userSignin } from '@/apis/home.js'
export default {
  name: 'signin',
  data: function() {
    return {
      email: null,
      password: null,
      remember: false,
      errors: {
        email: null,
        password: null,
        count: 0
      },
    }
  },
  computed: {
    emailState() {
      if( this.email === null)
        return null
      // return this.errors.email.length > 0 ? false : true
      if( this.errors.email === null ) {
        if(this.email.indexOf("@") > 0 && this.email.indexOf(".") > 0) {
          return true;
        }
        return false;
      } else {
        return false;
      }
    },
    passwordState() {
      if(this.password === null) 
        return null
      if( this.errors.password !== null)
        return false
      return this.password.length > 5 ? true : false
    }
  },
  methods: {
    toSignIn: function() {
      var params = {
        email: this.email,
        password: this.password,
        keep_signedin: this.remember
      }
      this.errors.email = null
      this.errors.password = null
      userSignin( params ).then( resp => {
        console.log(resp)
        if( resp.status === 'fail' ) {
          this.errors = resp;
          this.errors.count = 1;
        } else if( resp.status === 'success' ) {
          if(resp.level === 'user')
            window.location = '/user'
          else if(resp.level === 'admin')
            window.location = '/admin'

        }
      })
    }
  }
}
</script>
<style>

.form-signin {
  width: 400px;
  max-width: 430px;
  padding: 15px;
  margin: 0 auto;
}

@media screen and (max-width: 486px) {
  .form-signin {
    width: 100%;
    padding: 15px;
    margin-top: 50px;
  }
}

.form-signin .checkbox {
  font-weight: 400;
}
.form-signin .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}
.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>

