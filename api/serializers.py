from rest_framework import serializers
from api.models import *


class FarmSerializer(serializers.ModelSerializer):
	class Meta:
		model = Farm
		fields = '__all__'
		exclude = ()


class ContactSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contact
		fields = '__all__'
		exclude = ()


class FarmerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Farmer
		fields = '__all__'
		exclude = ()


class LoggerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Logger
		fields = '__all__'
		exclude = ()


class TemplateMessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = TemplateMessage
		fields = '__all__'
		exclude = ()


class OutboundMessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutboundMessage
		fields = '__all__'
		exclude = ()


class OutboundFarmerSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutboundFarmer
		fields = '__all__'
		exclude = ()


class InboundMessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = InboundMessage
		fields = '__all__'
		exclude = ()