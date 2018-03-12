from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
	def validation(self, postData, error_validation):
		errors = {}
		if error_validation == 'register':
			if len(postData['name']) < 3:
				errors['name'] = "Name must contain at least 3 letters!"
			if not NAME_REGEX.match(postData['name']):
				errors['name'] = "Name cannot be blank and can only contain letters!"
			elif len(postData['username']) < 3:
				errors['username'] = "Username must contain at least 3 letters!"
			elif not NAME_REGEX.match(postData['username']):
				errors['username'] = "Username cannot be blank and can only contain letters!"
			elif User.objects.filter(uername=postData['username']):
				errors['username'] = "Username already being used!"
			elif len(postData['pw']) < 9:
				errors['pw'] = "Password must contain more than 8 characters!"
			elif not postData['pw'] == postData['confirm_pw']:
				errors['pw'] = "Both passwords must match!"
		if error_validation == 'login':
			user = User.objects.filter(username=postData['user_login'])
			if not NAME_REGEX.match(postData['user_login']):
				errors['user_login'] = "Invalid username"
			elif not User.objects.filter(username=postData['user_login']):
				errors['user_login'] = "No username in system"
			elif not bcrypt.checkpw(postData['pw_login'].encode(), user[0].pw.encode()):
				errors['pw_login'] = "Invalid login and/or password!"
		return errors

class WishManager(models.Manager):
	def validation(self, postData):
		errors = {}
		if len(postData['item']) < 3:
			errors['item'] = "Item must contain more than 3 characters!"
		return errors

# one user can have many items
# one item can have many users
# one creator can create many items
# one item can have one creator

class User(models.Model):
	name 		= models.CharField(max_length=255)
	username 	= models.CharField(max_length=255)
	pw 			= models.CharField(max_length=255)
	objects 	= UserManager()
	def __unicode__(self):
		return self.name

class Item(models.Model):
	name		= models.CharField(max_length=255)
	created_at	= models.DateField(auto_now_add=True)
	users		= models.ManyToManyField(User, related_name='shared_items')
	creator		= models.ForeignKey(User, related_name='created_items')
	objects		= WishManager()
	def __unicode__(self):
		return self.name