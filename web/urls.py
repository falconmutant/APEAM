from django.conf.urls import url
from django.contrib.auth import views as auth_views

from web.views import *

urlpatterns = [
	url(r'^$', index_view),
	url(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
	url(r'^lock/$', lock_view),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^LoadProfile/$', LoadProfile.as_view()),
	url(r'^testing/$', testing),
]