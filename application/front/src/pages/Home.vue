<template>
  <div class="home">
		
  <div class="black-bg" v-if="update_open==true">
    <div class="white-bg">
      <h4>kv Update <button @click="update_open=false">X</button></h4> 
      <p> {{ update_data.key }} <input v-model="update_data.value"></p>
			<button @click="update_open=false">Update</button>
    </div>
  </div>

  <div class="black-bg" v-if="add_open==true">
    <div class="white-bg">
      <h4>kv Add <button @click="add_open=false">X</button></h4> 
      <p> <input v-model="add_data.key"> <input v-model="add_data.value"></p>
			<button @click="add_open=false">Add</button>
    </div>
  </div>

  <div class="app">
  <div v-if="local.getItem('name')"> 
    {{ local.getItem("name") }}, Hi 
    <button @click="logout()"> LogOut </button>
    <div v-if="local.getItem('team') === 'admin'"> 
      <h1>ADMIN</h1>
    </div>
    <div v-else> 
      <h1>USER</h1>
    </div>
  </div>
  <div v-else> 
    <label for="loginID">
      <span>ID</span>
      <input type="text" id="loginID" v-model="state.form.loginID"/>
    </label>
    <label for="loginPW">
      <span>PW</span>
      <input type="password" id="loginPW" v-model="state.form.loginPW"/>
      <hr />
      <button @click="login()">Login</button>
    </label>
  </div>
  </div>

  </div>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies"
import {reactive} from "vue";
import router from '@/routes.js'

export default {
  setup() {
    function localStorageSetItem(key, value) {
      localStorage.setItem(key, value)
    }
    const local = window.localStorage;
    
    const state = reactive({
      form:{
        loginID: "",
        loginPW: "",
      }
    });
    const login = () => {
      const args = {
        name: state.form.loginID,
        password: state.form.loginPW
      };
      axios.post(process.env.VUE_APP_API_IP+"/login", args, {withCredentials:true}).then((res)=>{
        localStorageSetItem('name', res.data.name);
        localStorageSetItem('team', res.data.team);
        localStorageSetItem('token', res.data.token);
        if (res.data.team == 'admin') {
          router.push('/admin')
        } else {
          router.push('/user')
        }
      }).catch((e) => {
        alert(e.response.data.result)
      });
    };

    const logout = () => {
        VueCookies.get("Authorization");
        VueCookies.keys().forEach(cookie => VueCookies.remove(cookie));

        localStorage.clear();
        router.go(0);
        };
    return {local, state, login, logout}
  }
}
</script>

<style scoped>

</style>