<template>
<RouterView/>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies"
import {reactive} from "vue";
import router from './routes.js'

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
      axios.post("http://13.208.122.114:8000/login", args, {withCredentials:true}).then((res)=>{
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

<style>
body {
  margin: 0
}
div {
  box-sizing: border-box;
}

.black-bg {
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.5);
  position: fixed; padding: 20px;
}
.white-bg {
  width: 100%;
  background: white;
  border-radius: 8px; padding: 20px;
}


#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.menu {
  background: darkslateblue;
  padding: 15px;
  border-radius: 5px;
}

.menu a{
  color: white;
  padding: 10px;
}
</style>
