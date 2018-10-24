from rest_framework import serializers
from web.models import *


class MenuSerializer(serializers.ModelSerializer):
	class Meta:
		model = Menu
		fields = '__all__'
		exclude = ()


class CoreGadgetSerializer(serializers.ModelSerializer):
	class Meta:
		model = CoreGadget
		fields = '__all__'
		exclude = ()


class GadgetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Gadget
		fields = '__all__'
		exclude = ()


class MenuGadgetSerializer(serializers.ModelSerializer):
	class Meta:
		model = MenuGadget
		fields = '__all__'
		exclude = ()


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = '__all__'
		exclude = ()
