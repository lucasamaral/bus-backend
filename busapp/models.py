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
    first_stop = models.ForeignKey(Stop, related_name="+")
    second_stop = models.ForeignKey(Stop, related_name="+")

    def __unicode__(self):
        return unicode(self.first_stop) + ' to ' + unicode(self.second_stop)


class BusLine(models.Model):
    name = models.CharField(max_length=30)
    number = models.CharField(max_length=20)
    segments = models.ManyToManyField(LineSegment, through='BusLineRelation')

    def get_start_segment(self):
        return BusLineRelation.objects.filter(bus_line=self).order_by('order').first().line_segment

    def get_end_segment(self):
        return BusLineRelation.objects.filter(bus_line=self).order_by('order').last().line_segment

    def __unicode__(self):
        return self.number + '-' + self.name


class BusLineRelation(models.Model):
    line_segment = models.ForeignKey(LineSegment)
    bus_line = models.ForeignKey(BusLine)
    order = models.IntegerField()

    def __unicode__(self):
        return unicode(self.bus_line) + '#' + str(self.order)
