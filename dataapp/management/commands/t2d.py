# -*- coding: utf-8 -*-
from datetime import datetime
import urllib2
import json
import random
from django.utils.encoding import smart_str, smart_unicode
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import  get_object_or_404
from django.contrib.sites.models import Site
from herbprofile.models import Experiment
from datautils import *
import os
import datautils.T2DConverter as T2dCon

class Command(BaseCommand):
    def handle(self, *args, **options):
        exp = Experiment.objects.all()[0]
        fullpath = exp.t2d_file.path
        path, filename_ext  = os.path.split(fullpath)
        filename, extension = os.path.splitext(filename_ext)
        ma, csv_path = T2dCon.data_converter(path,filename ,extension, path)
        det_peaks = T2dCon.get_peaks(ma)
        import pdb; pdb.set_trace()