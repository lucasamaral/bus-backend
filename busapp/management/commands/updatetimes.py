from django.core.management.base import BaseCommand

from busapp.models import BusLine, BusLineRelation


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_lines = BusLine.objects.all()
        relations = BusLineRelation.objects.filter(bus_line__in=all_lines)
        for rel in relations:
            times = rel.line_segment.timemeasured_set.all()
            time_ints = []
            for time in times:
                time_ints.append(time.time_value)
            if len(times) == 0:
                average = 0
            else:
                average = sum(time_ints)/len(times)

            rel.line_segment.time_estimated = int(average)
            rel.line_segment.save()
            self.stdout.write('Line:%s-Avg:%s' % (rel.line_segment.id, average))
