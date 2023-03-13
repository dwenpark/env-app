from django.urls import path

from info.views import InfosView, UsersView, TeamsView, TeamsDeleteView, UsersDeleteView, InfosDeleteView, LoginView, InfosGetView

urlpatterns = [
	path('infos', InfosView.as_view()),
	path('getinfos', InfosGetView.as_view()),
	path('users', UsersView.as_view()),
	path('teams', TeamsView.as_view()),
	path('delete/team', TeamsDeleteView.as_view()),
	path('delete/user', UsersDeleteView.as_view()),
	path('delete/info', InfosDeleteView.as_view()),
	path('login', LoginView.as_view()),
]