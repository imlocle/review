from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^books$', views.books),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^addbook$', views.addbook),
    url(r'^add$', views.add),
    url(r'^bookprofile/(?P<id>\d+)$', views.bookprofile),
    url(r'^addreview$', views.addreview),
    url(r'^userprofile/(?P<id>\d+)$', views.userprofile),




]
