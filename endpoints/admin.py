from django.contrib import admin
from .models import CrosswalkModel, TrafficModel, CCTVModel

admin.site.register(CrosswalkModel)
admin.site.register(TrafficModel)
admin.site.register(CCTVModel)
