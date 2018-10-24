import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from rest_framework.views import APIView

from web.serializers import *
from web.utils import *

# Create your views here.


def logout_view(request):
	logout(request)
	return redirect('/login/?next=/')


def lock_view(request):
	if request.POST:
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			username = request.POST['username']
			return render(request, 'registration/lock.html', locals())
	else:
		try:
			username = request.user.username
			logout(request)
			return render(request, 'registration/lock.html', locals())
		except Exception as e:
			return redirect('/login/?next=/Panel/')


@login_required
def index_view(request):
	profile = Profile.objects.get(user=request.user)
	image_profile = profile.config['image_profile']
	return render(request, 'base.html', locals())


@login_required
def testing(request):
	profile = Profile.objects.get(user=request.user)
	image_profile = profile.config['image_profile']
	return render(request, 'testing.html', locals())


class LoadProfile(APIView):
	def post(self, request):
		profile = request.user.profile
		data = {
			'gadgets': [],
			'menu': []
		}

		if request.data['target'] == 'initialize':
			menu_gadgets = MenuGadget.objects.filter(type=profile.type, alive=True).order_by('id')
			for menu in menu_gadgets:
				menu = MenuSerializer(menu.menu).data
				data['menu'].append(menu)

			gadgets = menu_gadgets[0].gadget.filter(alive=True).order_by('id')
			for gadget in gadgets:
				data['gadgets'].append(generate_gadget(gadget))

		elif request.data['target'] == 'menu':
			menu_gadgets = MenuGadget.objects.filter(id=request.data['data']['id']).order_by('id')
			gadgets = menu_gadgets.gadget.filter(alive=True).order_by('id')
			for gadget in gadgets:
				data['gadgets'].append(generate_gadget(gadget))

		data = json.dumps(data)
		return HttpResponse(data, content_type='application/json')
