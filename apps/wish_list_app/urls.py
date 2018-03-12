from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^dashboard$', views.dashboard),
	url(r'^create_item$', views.create_item),
	url(r'^create_item_process$', views.create_item_process),
	url(r'^add_wishlist/(?P<id>\d+)$', views.add_wishlist),
	url(r'^wish_items/(?P<id>\d+)$', views.wish_items),
	url(r'^remove_item/(?P<id>\d+)$', views.remove_item),
	url(r'^delete_item/(?P<id>\d+)$', views.delete_item),
	url(r'^logout$', views.logout)
]