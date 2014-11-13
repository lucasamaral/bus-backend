from django.db import models


class Point(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    def __unicode__(self):
        return 'Lat:%011.6f Lon:%011.6f' % (self.lat, self.lon)


class Stop(models.Model):
    name = models.CharField(blank=True, max_length=100)
    address = models.CharField(blank=True, max_length=200)
    point = models.OneToOneField(Point)

    def __unicode__(self):
        return self.address


class LineSegment(models.Model):
    first_stop = models.ForeignKey(Stop, related_name='first_stop')
    second_stop = models.ForeignKey(Stop, related_name='second_stop')
    points = models.ManyToManyField(Point, through='LinePointRelation')
    time_estimated = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.first_stop) + ' to ' + unicode(self.second_stop)


class TimeMeasured(models.Model):
    time_value = models.IntegerField()
    line_segment = models.ForeignKey(LineSegment)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Time: ' + unicode(self.time_value) + 'Dt: ' + unicode(self.created)


class LinePointRelation(models.Model):
    line_segment = models.ForeignKey(LineSegment)
    point = models.ForeignKey(Point)
    order = models.IntegerField()

    def __unicode__(self):
        return 'Point: ' + unicode(self.line_segment) + '#' + unicode(self.order)


class BusLine(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    segments = models.ManyToManyField(LineSegment, through='BusLineRelation')

    def get_start_segment(self):
        first = self.buslinerelation_set.all().order_by('order').first()
        if first:
            return first.line_segment
        else:
            return None

    def get_end_segment(self):
        last = self.buslinerelation_set.all().order_by('order').last()
        if last:
            return last.line_segment
        else:
            return None

    def stop_points(self):
        all_segs_ordered = self.buslinerelation_set.all().order_by('order')
        stops_pts_in = [{'point': seg.line_segment.second_stop.point, 'seg_id': seg.line_segment.id}
                        for seg in all_segs_ordered]
        stops_pts_in.insert(0, {'point': all_segs_ordered.first().line_segment.first_stop.point,
                                'seg_id': all_segs_ordered.first().id})
        return stops_pts_in

    def __unicode__(self):
        return self.number + '-' + self.name


class BusLineRelation(models.Model):
    line_segment = models.ForeignKey(LineSegment)
    bus_line = models.ForeignKey(BusLine)
    order = models.IntegerField()

    def __unicode__(self):
        return unicode(self.bus_line) + '#' + unicode(self.order)


class Bus(models.Model):
    departure_time = models.TimeField()
    bus_line = models.ForeignKey(BusLine)

    def __unicode__(self):
        return 'Bus ' + unicode(self.departure_time)
