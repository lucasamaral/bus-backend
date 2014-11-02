from django.contrib import admin
from busapp import models

admin.site.register(models.Point)
admin.site.register(models.Stop)
admin.site.register(models.TimeEstimation)
admin.site.register(models.LineSegment)
admin.site.register(models.LinePointRelation)
admin.site.register(models.BusLine)
admin.site.register(models.BusLineRelation)
admin.site.register(models.Bus)
