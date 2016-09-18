from herbprofile.models import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def convert_scientific_name(self):
        herbs = Herb.objects.all()
        for herb in herbs:
        	herb.scientific_name = herb.scientific_name.lower().capitalize()
        	herb.save()

    def handle(self, *args, **options):
        self.convert_scientific_name()
