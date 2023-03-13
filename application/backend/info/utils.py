import jwt

from django.http        import JsonResponse

from envapp.my_settings import SECRET_KEY, ALGORITHMS
from info.models        import User

def login_decorator(func):
	def wrapper(self, request, *args, **kwargs):
		try:
			access_token = request.headers.get("Authorization")
			payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHMS)
			user         = User.objects.get(id=payload["id"])
			request.user = user
		
		except jwt.exceptions.DecodeError:
			return JsonResponse({"MESSAGE" : "INVALID_TOKEN"}, status=400)
		
		except User.DoesNotExist:
			return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=400)
    
		return func(self, request, *args, **kwargs)
	return wrapper


def login_admin_decorator(func):
	def wrapper(self, request, *args, **kwargs):
		try:
			access_token = request.headers.get("Authorization")
			payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHMS)
			user         = User.objects.get(id = payload["id"])
			request.user = user

			if not user.team.name == "admin":
				return JsonResponse({"result" : "UNAUTHORIZED"}, status=403)

		except jwt.exceptions.DecodeError:
			return JsonResponse({"result" : "INVALID_TOKEN"}, status=400)
		
		except User.DoesNotExist:
			return JsonResponse({"result" : "INVALID_USER"}, status=400)
    
		return func(self, request, *args, **kwargs)
	return wrapper