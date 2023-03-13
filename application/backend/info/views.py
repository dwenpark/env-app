import json, jwt

from django.http        import JsonResponse
from django.views       import View
from django.utils       import timezone

from envapp.my_settings import SECRET_KEY, ALGORITHMS
from info.utils         import login_decorator, login_admin_decorator
from info.models        import User, Team, Info

class TeamsView(View):
	@login_admin_decorator
	def post(self, request):
		data = json.loads(request.body)

		if Team.objects.filter(name= data['name']).exists():
			return JsonResponse({"result" : "CONFILCT"}, status = 409)

		team = Team.objects.create(
			name = data['name']
			)
		return JsonResponse({'result':'created'}, status=201)
  
	@login_admin_decorator
	def get(self, request):
		teams   = Team.objects.all()
		results = []
		for team in teams:
			results.append(
				{
					"id"        : team.id,
					"team_name" : team.name
				}
			)
		return JsonResponse({'result': results}, status=200)

class TeamsDeleteView(View):
	@login_admin_decorator
	def post(self, request):
		data = json.loads(request.body)
		team = Team.objects.filter(id= data['id'])

		if not team.exists() :
			return JsonResponse({"result" : "NO_DELETE"}, status = 404)

		if team[0].name == "admin":
			return JsonResponse({"result" : "UNAUTHORIZED"}, status = 403)

		try:
			team.delete()
			return JsonResponse({'result':'deleted'}, status=204)

		except KeyError:
			return JsonResponse({'result':"KEY_ERROR"}, status=400)

class UsersView(View):
	@login_admin_decorator
	def post(self, request):
		data = json.loads(request.body)

		if User.objects.filter(name= data['name']).exists():
			return JsonResponse({"result" : "CONFILCT"}, status = 409)

		user = User.objects.create(
			name     = data['name'],
			password = data['name'],
			team     = Team.objects.get(name = data['team'])
			)
		return JsonResponse({'result':'created'}, status=201)
  
	def get(self, request):
		users   = User.objects.all()
		results = []
		for user in users:
			results.append(
				{
					"id"         : user.id,
					"user_name"  : user.name,
					"user_team"  : user.team.name
				}
			)
		return JsonResponse({'result': results}, status=200)
  
	@login_admin_decorator
	def patch(self, request):
		try:
			data = json.loads(request.body)
			user = User.objects.filter(id = data["id"]).update(password= data.get("password"))
			return JsonResponse({'result':"updated"}, status=201)

		except KeyError:
			return JsonResponse({'result':"KEY_ERROR"}, status=400)

class UsersDeleteView(View):
	@login_admin_decorator
	def post(self, request):
		data = json.loads(request.body)
		user = User.objects.filter(id= data['id'])

		if not user.exists() :
			return JsonResponse({"result" : "NO_DELETE"}, status = 404)

		if user[0].name == "admin":
			return JsonResponse({"result" : "UNAUTHORIZED"}, status = 403)

		try:
			user.delete()
			return JsonResponse({'result':'deleted'}, status=204)

		except KeyError:
			return JsonResponse({'result':"KEY_ERROR"}, status=400)


class InfosView(View):
	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
		user = request.user

		info = Info.objects.create(
			user  = User.objects.get(name = data['user']),
			team  = Team.objects.get(name = data['team']),
			key   = data['key'],
			value = data['value'],
			time  = timezone.now()
			)
		return JsonResponse({'result':'created'}, status=201)
  
	@login_decorator
	def patch(self, request):
		try:
			data = json.loads(request.body)
			user = request.user

			info = Info.objects.filter(id = data["id"]).update(user_id= User.objects.get(name= data.get("user")).id, value= data.get("value"), time=timezone.now())
			return JsonResponse({'result':"updated"}, status=201)

		except KeyError:
			return JsonResponse({'result':"KEY_ERROR"}, status=400)

class InfosGetView(View):
	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
		infos   = Info.objects.filter(team = Team.objects.get(name=data.get("team")))
		results = []

		for info in infos:
			results.append(
				{
					"id"        : info.id,
					"user_name" : info.user.name,
					"user_team" : info.team.name,
					"key"       : info.key,
					"value"     : info.value,
					"time"      : info.time
				}
			)
		return JsonResponse({'result':results}, status=200)

class InfosDeleteView(View):
	@login_decorator
	def post(self, request):
		data = json.loads(request.body)
		user = request.user

		info = Info.objects.filter(id= data['id'])

		if not info.exists() :
			return JsonResponse({"result" : "NO_DELETE"}, status = 404)

		try:
			info.delete()
			return JsonResponse({'result':'deleted'}, status=204)

		except KeyError:
			return JsonResponse({'result':"KEY_ERROR"}, status=400)


class LoginView(View):
	def post(self, request):
		if request.headers.get("Authorization"):
			access_token = request.headers.get("Authorization")
			payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHMS)
			logging_user = User.objects.get(id = payload["id"])

		else:
			data = json.loads(request.body)
			user = User.objects.filter(
				name = data['name']
				)

			if not user.exists() :
				return JsonResponse({"result" : "USER_NOT_FOUND"}, status = 404)
			
			logging_user = User.objects.get(name = data['name'])

			if not logging_user.password == data['password']:
				return JsonResponse({"result" : "PW_ERROR"}, status = 401)
		
		token = jwt.encode({'id' : logging_user.id}, SECRET_KEY, algorithm = ALGORITHMS)
		res = JsonResponse({'result':'success',  'token': token, 'name': logging_user.name, 'team': logging_user.team.name}, status=200)
		res.set_cookie('Authorization', token, samesite='Lax', max_age=600)
		res.set_cookie('name', logging_user.name, samesite='Lax', max_age=600)
		res.set_cookie('team', logging_user.team.name, samesite='Lax', max_age=600,)
		return res
		