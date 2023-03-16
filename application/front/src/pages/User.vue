<template>
  <div class="black-bg" v-if="info_update_open==true">
    <div class="white-bg">
      <h4>kv Update <button @click="info_update_open=false">X</button></h4> 
      <p> {{ tmp_key }} / {{ tmp_value }} </p>
      <p> update_value: <input v-model="info_update_data.value"></p>
			<button @click="info_update_open=false, updateInfo(tmp_kv_id,tmp_key,info_update_data.value)">Update</button>
    </div>
  </div>

  <div class="black-bg" v-if="info_add_open==true">
    <div class="white-bg">
      <h4>kv Add <button @click="info_add_open=false">X</button></h4> 
      <p> <input v-model="info_add_data.key"> <input v-model="info_add_data.value"></p>
			<button @click="info_add_open=false, postInfo(info_add_data.key, info_add_data.value)">Add</button>
    </div>
  </div>

	<h1>User</h1>
  <button @click="logout()"> LogOut </button>


  <h4>key / value / user / updated_time </h4>
  <button @click="info_add_open=true">Add Info</button>
  <div v-for="kv in info" :key="kv">
  <p>
    {{ kv.key }} / {{ kv.value }} / {{ kv.user_name }} / {{ kv.time }}
    <button @click="info_update_open=true, tmp_key=kv.key, tmp_value=kv.value, tmp_kv_id=kv.id">Update</button>
    <button @click="deleteInfo(kv.id)">Delete</button>
  </p>
  </div>
</template>

<script>
import VueCookies from "vue-cookies"
import router from '@/routes.js'
import axios from 'axios'

export default {
	created() {
    const local = window.localStorage;
    const args = {
      token: local.getItem("token"),
      user: local.getItem("name"),
      team: local.getItem("team")
    };
    const headers = { "Authorization" : local.getItem("token")};
    axios.post(process.env.VUE_APP_API_IP+"/getinfos", args,{headers}, {withCredentials:true}).then((res)=>{
      this.info = res.data.result;
    }).catch((e) => {
      alert(e.response.data.result);
    });
    },
  setup() {
    const logout = () => {
        VueCookies.get("Authorization");
        VueCookies.keys().forEach(cookie => VueCookies.remove(cookie));

        localStorage.clear();
        router.push('/');
        };

    const postInfo = (key, value) => {
      const local = window.localStorage;
      const args = {
        key: key,
        value: value,
        user: local.getItem('name'),
        team: local.getItem("team")
      };
      const headers = { "Authorization" : local.getItem("token")}
      axios.post(process.env.VUE_APP_API_IP+"/infos", args, {headers}, {withCredentials:true}).then(()=>{
        router.go(0)
      }).catch((e) => {
        alert(e.response.data.result)
      });
    };

   const updateInfo = (id,key,value) => {
      const local = window.localStorage;
      const args = {
        id: id,
        key: key,
        value: value,
        user: local.getItem('name'),
        team: local.getItem("team")
      };
      const headers = { "Authorization" : local.getItem("token")}
      axios.patch(process.env.VUE_APP_API_IP+"/infos", args, {headers}, {withCredentials:true}).then(()=>{
        router.go(0)
      }).catch((e) => {
        alert(e.response.data.result)
      });
    };

    const deleteInfo = (info_id) => {
    const local = window.localStorage;
      const args = {
        id: info_id
      };
      const headers = { "Authorization" : local.getItem("token")}
      axios.post(process.env.VUE_APP_API_IP+"/delete/info", args, {headers}, {withCredentials:true}).then(()=>{
        router.go(0)
      }).catch((e) => {
        alert(e.response.data.result)
      });
    };

    return {logout, postInfo, deleteInfo, updateInfo}
  },
  data(){
    return {
      info : null,
      info_update_data: {},
      info_update_open: false,
      info_add_data: {},
      info_add_open: false,
      tmp_key: null,
      tmp_value: null,
      tmp_kv_id: null
    }
	}
}

</script>

<style scoped>

</style>