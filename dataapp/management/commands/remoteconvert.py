import requests
from django.core.management.base import BaseCommand
from dataapp.models import *
from django.conf import settings

class Command(BaseCommand):
    def call_process(self):
        for profile_row in Order.objects.all():
            # if not profile_row.csv_file:
                url = settings.REMOTE_SERVICE_ADDR
                process_url = url + 'dataapp/process2/%d' % profile_row.pk
                print process_url
                ret = requests.get(process_url)
                # print ret.json()

    def handle(self, *args, **options):
        self.call_process()