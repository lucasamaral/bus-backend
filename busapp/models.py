from django.db import models


class Point(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    def __unicode__(self):
        return 'Lat:' + str(self.lat) + 'Lon:' + str(self.lon)


class Stop(models.Model):
    name = models.CharField(blank=True, null=True, max_length=50)
    address = models.CharField(max_length=50)
    point = models.OneToOneField(Point)
    def __unicode__(self):
        return self.address