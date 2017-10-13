from __future__ import absolute_import
from django.db.models import Max
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
import os
from os.path import basename
from django.conf import settings
from django.utils.safestring import mark_safe
import datetime
from django.views.generic import CreateView, UpdateView, DeleteView
import account.views
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
import requests
import zipfile
import StringIO
from pprint import pprint
import random
from django.core.mail import send_mail

@csrf_exempt
def voucher_api(request):
    if request.method == 'POST':
        email = request.POST.get('email' , None)
        voucher = request.POST.get('voucher' , "")

        if email == None:
            data = {}
            return HttpResponse(json.dumps(data), mimetype='application/json')

        send_mail(
            'Voucher For you!',
            'Congratulation! You receive the voucher of ' + voucher,
            'admin@flashfeedback.com',
            [email],
            fail_silently=False,
        )

        data = {'success' : 1}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    else:
        return HttpResponse("{}", mimetype='application/json')

@csrf_exempt
def post_api(request):
    if request.method == 'POST':
        product_id = request.POST.get('product' , None)

        if product_id == None:
            return HttpResponse("[]", mimetype='application/json')

        product = Product.objects.get(pk = product_id)

        email = request.POST.get('email' , None)

        if email == None:
            return HttpResponse("[]", mimetype='application/json')

        user = UserProfile.objects.get(email = email)

        like = request.POST.get('like' , None)

        if like == None:
            return HttpResponse("[]", mimetype='application/json')

        record = Record(user = user , product = product , like = like)
        record.save()

        data = {'success' : 1}
        return HttpResponse(json.dumps(data), mimetype='application/json')
    else:
        return HttpResponse('[]', mimetype='application/json')

@csrf_exempt
def product_api(request):
    if request.method == 'GET':
        email = request.GET.get('email' , None)

        if email == None:
            return HttpResponse('[]', mimetype='application/json')
 
        userprofile = UserProfile.objects.filter(email = email)

        if len(userprofile) == 0:
            return HttpResponse('[]', mimetype='application/json')

        user_info = userprofile[0]

        products = Product.objects.filter(startAge__lt = user_info.age).filter(hidden = 0).filter(endAge__gt = user_info.age).filter(Q(targetGender = user_info.gender) | Q(targetGender = 3))

        interests = user_info.getInterests()

        data = []

        for product in products:
            data.append(product.getData())

        return HttpResponse(json.dumps(data), mimetype='application/json')
    else:
        return HttpResponse('[]', mimetype='application/json')

def home_view(request):
    return render_to_response("dataapp/home.html", {
        }, RequestContext(request))

@login_required
def product_list_view(request):
    user = request.user

    company = Company.objects.filter(user = user)

    if not company:
        return redirect('/')

    company = company[0]
    products = Product.objects.filter(company = company)

    for product in products:
        total = Record.objects.filter(product = product)
        likes = total.filter(like = 'y').count()
        dislikes = total.count() - likes

        product.likes = likes
        product.dislikes = dislikes

    return render_to_response("dataapp/product_list.html", {
        'products': products,
        'company':company
        }, RequestContext(request))
