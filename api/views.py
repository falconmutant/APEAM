import json
from datetime import datetime

from django.db import transaction
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView

from api.serializers import *

# Create your views here.


class TablesRest(APIView):
	def post(self, request):
		if request.data['target'] == 'table':
			if request.data['category'] == 'initialize':
				data = {
					'data': [
						{
							'Nombre': '',
							'Registro': '',
							'Fecha': '',
							'Acciones': ''
						}
					]
				}
			elif request.data['category'] == 'load':
				data = {
					'data': []
				}

		data = json.dumps(data)
		return HttpResponse(data, status=status.HTTP_200_OK, content_type='json/application')


class FarmerRest(APIView):
	@transaction.atomic
	def post(self, request):
		if request.data['target'] == 'farmer':
			if request.data['action'] == 'get':
				farmer = Farmer.objects.get(id=request.data['data']['id'])
				farmer = FarmerSerializer(farmer)
				data = farmer.data
			elif request.data['action'] == 'all':
				farmers = Farmer.objects.filter(user=request.user, alive=True)
				farmers = FarmerSerializer(farmers, many=True)
				data = farmers.data
			elif request.data['action'] == 'save':
				request.data._mutable = True

				farm = FarmSerializer(data=request.data['data']['farm'])
				if farm.is_valid():
					farm.save()
					request.data['farmer']['farm'] = farm.data['id']
				else:
					return HttpResponse(farm.errors, status=status.HTTP_400_BAD_REQUEST, content_type='json/application')

				request.data['farmer']['contact'] = []
				for contact in request.data['data']['contact']:
					contact = ContactSerializer(data=contact)
					if contact.is_valid():
						contact.save()
						request.data['farmer']['contact'].append(contact.data['id'])
					else:
						transaction.rollback(True)
						return HttpResponse(contact.errors, status=status.HTTP_400_BAD_REQUEST, content_type='json/application')

				request.data['farmer']['created_by'] = request.user.id
				request.data['farmer']['created'] = datetime.today()
				request.data['farmer']['alive'] = True
				farmer = FarmerSerializer(data=request.data['data']['farmer'])
				if farmer.is_valid():
					farmer.save()
					data = farmer.data
				else:
					transaction.rollback(True)
					return HttpResponse(farmer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='json/application')
			elif request.data['action'] == 'modify':
				request.data._mutable = True
				request.data['updated_by'] = request.user.id
				request.data['updated'] = datetime.today()

				farmer = Farmer.objects.get(id=request.data['data']['id'])
				farmer = FarmerSerializer(farmer, data=request.data['data'], partial=True)
				if farmer.is_valid():
					farmer.save()
					data = farmer.data
				else:
					return HttpResponse(farmer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='json/application')
			elif request.data['action'] == 'delete':
				farmer = Farmer.objects.get(id=request.data['data']['id'])
				farmer.alive = False
				farmer.save()
				data = 'Farmer Deleted'

		elif request.data['target'] == 'contact':
			if request.data['action'] == 'get':
				pass
		data = json.dumps(data)
		return HttpResponse(data, status=status.HTTP_200_OK, content_type='json/application')
