from django.shortcuts import render, HttpResponse, redirect
from django.contrib.messages import error
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
	return render(request, 'index.html')

def register(request):
	errors = User.objects.validation(request.POST, 'register')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
			return redirect('/')
	else:
		new_user = User.objects.create(
			name		= request.POST['name'],
			username 	= request.POST['username'],
			pw			= bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()))
		request.session['name'] = new_user.name
		request.session['id']	= new_user.id
	return redirect('/dashboard')

def login(request):
	errors = User.objects.validation(request.POST, 'login')
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
		return redirect('/')
	else:
		login_user = User.objects.get(username=request.POST['user_login'])
		request.session['name']	= login_user.name
		request.session['id']	= login_user.id
	return redirect('/dashboard')

def dashboard(request):
	if 'id' not in request.session:
		return redirect('/')
	this_user = User.objects.get(id=request.session['id'])
	context = {
			# join manytomanyfield and foreignkeys between users and items
			"user_items": this_user.shared_items.all().order_by('-created_at'),
			"all_items": Item.objects.all().exclude(users=request.session['id']).exclude(creator_id=request.session['id']).order_by('-created_at')
		}
	return render(request, 'dashboard.html', context)

def create_item(request):
	if 'id' not in request.session:
		return redirect('/')
	return render(request, 'create_item.html')

def create_item_process(request):
	errors = Item.objects.validation(request.POST)
	if len(errors):
		for error in errors.itervalues():
			messages.error(request, error)
			return redirect('/create_item')
	else:
		new_item = Item.objects.create(
			name		= request.POST['item'],
			creator_id 	= request.session['id'])
		new_item.users.add(request.session['id'])
	return redirect('/dashboard')

def add_wishlist(request, id):
	this_user = User.objects.get(id=request.session['id'])
	this_item = Item.objects.get(id=id)
	this_user.shared_items.add(this_item)
	return redirect('/dashboard')

def wish_items(request, id):
	if 'id' not in request.session:
		return redirect('/')
	context = {
		"this_item": Item.objects.get(id=id),
		"shared_users": Item.objects.get(id=id).users.all().exclude(id=request.session['id'])
	}
	return render(request, 'wish_items.html', context)

def remove_item(request, id):
	this_user = User.objects.get(id=request.session['id'])
	this_item = Item.objects.get(id=id)
	this_user.shared_items.remove(this_item)
	return redirect('/dashboard')

def delete_item(request, id):
	this_item = Item.objects.get(id=id)
	this_item.delete()
	return redirect('/dashboard')

def logout(request):
	request.session.clear()
	return redirect('/')