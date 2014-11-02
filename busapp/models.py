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


class TimeEstimation(models.Model):
    time_value = models.IntegerField()

    def __unicode__(self):
        return 'Time: ' + unicode(self.time_value)


class LineSegment(models.Model):
    first_stop = models.ForeignKey(Stop, related_name='first_stop')
    second_stop = models.ForeignKey(Stop, related_name='second_stop')
    time_estimation = models.OneToOneField(TimeEstimation)
    points = models.ManyToManyField(Point, through='LinePointRelation')

    def __unicode__(self):
        return unicode(self.first_stop) + ' to ' + unicode(self.second_stop)


class LinePointRelation(models.Model):
    line_segment = models.ForeignKey(LineSegment)
    point = models.ForeignKey(Point)
    order = models.IntegerField()

    def __unicode__(self):
        return 'Point: ' + unicode(self.line_segment) + '#' + unicode(self.order)


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
        return unicode(self.bus_line) + '#' + unicode(self.order)


class Bus(models.Model):
    departure_time = models.DateTimeField()
    bus_line = models.ForeignKey(BusLine)
    # estimated_times = models.ManyToManyField(TimeEstimation, through='BusEstimationRelation')

    def __unicode__(self):
        return 'Bus ' + unicode(self.departure_time)


# class BusEstimationRelation(models.Model):
#     time_estimation = models.ForeignKey(TimeEstimation)
#     bus = models.ForeignKey(Bus)
#     order = models.IntegerField()

#     def __unicode__(self):
#         return self.bus.bus_line.number + ' ' + unicode(self.time_estimation) + '#' + unicode(self.order)
