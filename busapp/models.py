from django.db import models


class Point(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    def __unicode__(self):
        return 'Lat:%011.6fLon:%011.6f' % (self.lat, self.lon)


class Stop(models.Model):
    name = models.CharField(blank=True, null=True, max_length=50)
    address = models.CharField(max_length=50)
    point = models.OneToOneField(Point)
    def __unicode__(self):
        return self.address


class LineSegment(models.Model):
    firstStop = models.ForeignKey(Stop, related_name="first_stop")
    secondStop = models.ForeignKey(Stop, related_name="second_stop")
    def __unicode__(self):
        return unicode(self.firstStop) + ' to ' + unicode(self.secondStop)
