from django.conf.urls import url

from api.views import *

urlpatterns = [
	url(r'^Farmer/$', FarmerRest.as_view()),
	url(r'^TablesRest/$', TablesRest.as_view()),
]
