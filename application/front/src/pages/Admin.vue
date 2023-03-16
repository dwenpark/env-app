<template>
  <div>
    This is Admin Page
  </div>
  <button @click="logout()"> LogOut </button>

  <div class="black-bg" v-if="team_add_open==true">
    <div class="white-bg">
      <h4>Team Add <button @click="team_add_open=false">X</button></h4> 
      <h4> team </h4>
      <p> <input v-model="team_add_data.name"> </p>
			<button @click="team_add_open=false, postTeam(team_add_data.name)">Add</button>
    </div>
  </div>

  <div class="black-bg" v-if="user_add_open==true">
    <div class="white-bg">
      <h4>User Add <button @click="user_add_open=false">X</button></h4> 
      <h4>name / team </h4>
      <p> <input v-model="user_add_data.name"> <input v-model="user_add_data.team"></p>
			<button @click="user_add_open=false, postUser(user_add_data.name, user_add_data.team)">Add</button>
    </div>
  </div>

  <h4>name / team </h4>
  <button @click="team_add_open=true">Add Team</button>
  <button @click="user_add_open=true">Add User</button>
  <div v-for="kv in info" :key="kv">
  <p>
    {{ kv.user_name }} / {{ kv.user_team }}
    <button @click="deleteUser(kv.id)">Delete</button>
  </p>
</div>
</template>

<script>
import VueCookies from "vue-cookies"
import router from '@/routes.js'
import infos from '@/api/info';
import axios from 'axios';

export default {
	mounted() {
		infos.getUsers()
		.then((response) => {
      console.log(response.data.result);
      this.info = response.data.result;
		})
		.catch((e) => {
			console.log(e);
		});
	},
  setup() {
    const local = window.localStorage;

    const logout = () => {
        VueCookies.get("Authorization");
        VueCookies.keys().forEach(cookie => VueCookies.remove(cookie));

        localStorage.clear();
        router.push('/');
        };

    const postTeam = (name) => {
      const args = {
        name: name
      };
      const headers = { "Authorization" : local.getItem("token")}
      axios.post(process.env.VUE_APP_API_IP+"/teams", args, {headers}, {withCredentials:true}).then((res)=>{
        console.log(res.data)
        router.go(0)
      }).catch((e) => {
        alert(e.response.data.result)
      });
    };

    const postUser = (user, team) => {
      const args = {
        name: user,
        team: team
      };
      const headers = { "Authorization" : local.getItem("token")}
      axios.post(process.env.VUE_APP_API_IP+"/users", args, {headers}, {withCredentials:true}).then((res)=>{
        console.log(res.data)
        router.go(0)
      }).catch((e) => {
        alert(e.response.data.result)
      });
    };
    
    const deleteUser = (user_id) => {
      const args = {
        id: user_id
      };
      const headers = { "Authorization" : local.getItem("token")}
      axios.post(process.env.VUE_APP_API_IP+"/delete/user", args, {headers}, {withCredentials:true}).then((res)=>{
        console.log(res.data)
        router.go(0)
      }).catch((e) => {
        alert(e.response.data.result)
      });
    };
    return {logout, postTeam, postUser, deleteUser}

    
  },
  data(){
    return {
      info : null,
      team_add_data: {},
      team_add_open: false,
      user_add_data: {},
      user_add_open: false
    }
	}
}

</script>