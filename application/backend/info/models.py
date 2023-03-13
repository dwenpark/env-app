from django.db import models

class User(models.Model):
	name     = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	team     = models.ForeignKey('Team', on_delete=models.CASCADE)
		
	class Meta:
		db_table = 'users'

class Team(models.Model):
	name = models.CharField(max_length=20)

  
	class Meta:
		db_table = 'teams'

class Info(models.Model):
	key   = models.CharField(max_length=1000)
	value = models.CharField(max_length=1000)
	team  = models.ForeignKey('Team', on_delete=models.CASCADE)
	user  = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
	time  = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'infos'