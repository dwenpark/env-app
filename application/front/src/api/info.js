import axios from "axios";

const BASE_URL = "http://13.208.122.114:8000";

export default{

	getUsers: function() {
		return axios.get(BASE_URL + '/users')
	},
	getTeams: function() {
		return axios.get(BASE_URL + '/teams')
	},
	
	postTeam: function() {
		return axios.get(BASE_URL + '/users')
	},
	
	postUser: function(user, team, token) {
		const args = {
			"user" : user,
			"team" : team
		}
		const headers = { "Authorization": token }
		return axios.post(BASE_URL + '/users', args, {headers}, {withCredentials : true})
	},

	getInfos: function(token) {
		const headers = { "Authorization": token }
		return axios.post(BASE_URL + '/getinfos', {headers}, {withCredentials : true})
	},

	deleteUser: function() {
		return axios.post(BASE_URL + '/delete/user')
	},
	
	login: function() {
		return axios.post(BASE_URL + '/login')
	},
	
}