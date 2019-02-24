<template>
  <div class="card rounded-0 text-left form-signup">
    <div class="card-header">
      <h3 class="mb-0">Please Sign Up</h3>
    </div>
    <div class="card-body">
      <form class="form needs-validation" role="form" autocomplete="off" method="post">
        <div class="form-group">
          <label for="emailaddr" class="sr-only">Email address</label>
          <input type="email" id="emailaddr" name="email" class="form-control" placeholder="Email address" required autofocus="" 
            v-model="email" 
            v-bind:class="{ 'is-invalid': errors.code }" />
          <div class="invalid-feedback" v-if="errors.email">{{ errors.email }}</div>
        </div>
        <div class="form-group row">
          <label for="signupPassword" class="sr-only">Password</label>
          <div class="controls col-md-8 ">
            <input type="password" id="signupPassword" name="password" class="form-control mb-1" placeholder="Password" required="" 
              v-model="password" 
              v-bind:class="{ 'is-invalid': errors.password }" 
              v-if="!showPassword" />
            <input type="text" id="signupPassword" name="password" class="form-control mb-1" placeholder="Password" required="" 
              v-model="password" 
              v-bind:class="{ 'is-invalid': errors.password }" 
              v-if="showPassword" />
          </div>
          <label class="col-md-4 mt-2">
            <input type="checkbox" v-on:click="showPassword = !showPassword"> {{ 'Show' }}
          </label>
          <div class="invalid-feedback d-block px-3" v-if="errors.password">{{ errors.password }}</div>
        </div>
        <div class="form-group">
          <div class="row">
            <label for="checkcode" class="sr-only">CheckCode</label>
            <div class="controls col-md-8">
              <input type="text" class="form-control d-block"  id="checkcode" name="checkcode" placeholder="CheckCode" required v-model="code" 
                v-bind:class="{ 'is-invalid': errors.code }">
            </div>
            <button class="btn btn-primary col-md-3" type="button" v-on:click="sendCode()" >Get Code</button>
            <div class="invalid-feedback px-3 d-block" v-if="errors.code">{{ errors.code }}</div>
          </div>
        </div>
        <div class="form-group">
          <div class="form-check">
            <input type="checkbox" class="form-check-input" required id="agreement" v-model="aggrement" v-bind:class="{ 'is-invalid': errors.aggrement }"> I have read the <a href="#">agreement of usage</a>.
            <div class="invalid-feedback">{{ errors.aggrement }}</div>
          </div>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="button" v-on:click="toSignup()">Sign up</button>
        <p class="mt-5 mb-3 text-muted text-right">© 2017-2018</p>
      </form>
    </div>
    <!--/card-block-->
  </div>
</template>

<script>
import {sendCheckCode, userSignup} from '@/apis/home.js'

export default {
  name: 'signup',
  data: function() {
    return {
      aggrement: false,
      email: null,
      password: null,
      code: null,
      showPassword: false,
      errors: {
        aggrement: null,
        email: null,
        password: null,
        code: null
      }
    }
  },
  methods: {
    checkEmail: function() {
      if( !this.email ) {
        this.errors.email = "Input Your Email";
      } else {
        if( !this.validEmail( this.email )) {
          this.errors.email = "Valid Email Required";
        } else {
          this.errors.email = null
        }
      }
    },
    checkCode: function() {
      if( !this.code ) {
        this.errors.code = "Check Code Required.";
      } else {
        this.errors.code = null;
      }
    },
    checkPassword: function() {
      if( !this.password ) {
        this.errors.password = "Password Required.";
      } else {
        this.errors.password = null;
      }
    },
    checkAggrement: function() {
      if(! this.aggrement ) {
        this.errors.aggrement = "You must agree before sign up.";
      } else {
        this.errors.aggrement = null;
      }
    },
    sendCode: function() {
      this.checkEmail()
      if( !this.errors.email ) {
        // TODO show success information
        var params = {
          email: this.email
        }
        sendCheckCode( params ).then( resp => {
          console.log( resp )
          if( resp.status === 'fail' ) {
            this.errors.code = resp.desc;
          } else if( resp.status === 'success' ) {
            alert('验证码发送成功')
          }
        })
        return false;
      }
    },
    toSignup: function() {
      this.checkEmail()
      this.checkCode()
      this.checkPassword()
      this.checkAggrement()
      if( this.errors.aggrement || this.errors.code || this.errors.password || this.errors.email ) {
        return;
      }

      userSignup({ 
        email: this.email, 
        password: this.password, 
        checkcode: this.code,
      }).then( resp => {
        // console.log( resp )
        if( resp.status === 'success' ) {
          window.location = '/user'
        } else {
          this.errors = resp
        }
      })
    },
    validEmail: function (email) {
      var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }
  },
  mounted: function() {

  }
}
</script>

<style>

.form-signup {
  width: 450px;
  max-width: 450px;
  padding: 15px;
  margin: 0 auto;
}

.form-signup .checkbox {
  font-weight: 400;
}
.form-signup .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
.form-signup .form-control:focus {
  z-index: 2;
}
.form-signup input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-signup input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
