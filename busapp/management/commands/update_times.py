from django.core.management.base import BaseCommand

from busapp.models import BusLine, BusLineRelation


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_lines = BusLine.objects.all()
        relations = BusLineRelation.objects.filter(bus_line__in=all_lines)
        for rel in relations:
            times = rel.line_segment.timemeasured_set
            average = reduce(lambda x, y: x.time_value + y.time_value)/len(times)
            rel.line_segment.time_estimated = int(average)
            rel.line_segment.save()
            self.stdout.write('Line:%s-Avg:%s' % (rel.line_segment.id, average))
