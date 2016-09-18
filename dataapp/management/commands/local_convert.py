# -*- coding: utf-8 -*-
import requests
from django.core.management.base import BaseCommand
from herbprofile.models import *
from django.conf import settings
from django.db.models import Max
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.conf import settings
from datautils import *
import datetime
from datetime import datetime, date
import os
import csv
import json
import random
import datautils.T2DConverter as T2dCon
from django.utils.encoding import smart_str
from django.utils.translation import ugettext
from easy_thumbnails.files import get_thumbnailer
from django.utils import simplejson
from utils.batch_upload import *
from zipfile import *
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import ast
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
import xlsxwriter
import requests
import json
import numpy as np

class Command(BaseCommand):
    def call_process(self):
        for herbprofile in HerbProfile.objects.all():
            if not herbprofile.csv_file:
                t2dfile_path = herbprofile.file_object.path
                path, filename_ext = os.path.split(t2dfile_path)
                filename, extension = os.path.splitext(filename_ext)
                csv_path = herbprofile.file_object.url
                length = len(csv_path)-4
                csv_path = csv_path[:length]+".csv"
                herbprofile.csv_file = csv_path
                herbprofile.save()
                csv_path, mzxml_path, mz_array = T2dCon.data_converter(path,filename ,extension, path)
                T2dCon.decon_thrash_mzXML(mz_array, mzxml_path, 'parameter/SampleParameterFile.xml', 'decon/', 'data/output/')

                det_peaks = T2dCon.get_peaks(ma)

                # call the module by Liu Yong to get peaks from csv
                # peaks = get_peaks(new_exp.array_file)
                # save peaks into Peak table
                '''
                for peaks in det_peaks:
                    peak = Peak(herbprofile_id=herbprofile.id, mz=peaks[0], intensity=peaks[1])
                    peak.save()
                '''

    def handle(self, *args, **options):
        self.call_process()
