from django.contrib import admin
from api.models import *
# Register your models here.
admin.site.register(Farm)
admin.site.register(Contact)
admin.site.register(Farmer)
admin.site.register(Logger)
admin.site.register(TemplateMessage)
admin.site.register(OutboundMessage)
admin.site.register(OutboundFarmer)
admin.site.register(InboundMessage)
