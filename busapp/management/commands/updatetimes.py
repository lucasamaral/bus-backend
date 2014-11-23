from django.core.management.base import BaseCommand

from busapp.models import BusLine, BusLineRelation


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_lines = BusLine.objects.all()
        relations = BusLineRelation.objects.filter(bus_line__in=all_lines)
        for rel in relations:
            times = rel.line_segment.timemeasured_set.all()
            if len(times) == 0:
                average = 0
            elif len(times) == 1:
                average = times[0].time_value
            else:
                average = reduce(lambda x, y: x.time_value + y.time_value, times)/len(times)

            rel.line_segment.time_estimated = int(average)
            rel.line_segment.save()
            self.stdout.write('Line:%s-Avg:%s' % (rel.line_segment.id, average))
