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
import csv
import json
import requests
import zipfile
import StringIO
from pprint import pprint
import random
from PIL import Image
from django.core.mail import send_mail

DATA_ERROR = 1

def resize_uploaded_image(buf):
  imagefile = StringIO.StringIO(buf.read())
  imageImage = Image.open(imagefile)

  resizedImage = imageImage.resize((300,450))
  return resizedImage

# Create your views here.
class SignupView(account.views.SignupView):
   form_class = account.forms.SignupForm

   def after_signup(self, form):
       # print "aaaaaaaaaaaaaaaaaaaaaaaaaa"
       self.create_profile(form)
       super(SignupView, self).after_signup(form)

   def create_profile(self, form):
       userProfile = UserProfile(user=self.created_user)
       userProfile.save()

@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        data = request.POST.get('data' , None)

        if data == None:
            data = {}
            return HttpResponse(json.dumps(data), mimetype='application/json')

        age = request.POST.get('age' , 0)
        interests = request.POST.get('interests' , None)

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

def export_data(request , product_id):
    user = request.user

    company = Company.objects.filter(user = user)

    if not company:
        return redirect('/')

    company = company[0]
    product = get_object_or_404(Product , pk = product_id)

    records = Record.objects.filter(product = product)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + product.title + '.csv"'

    fields = ['email' , 'age' , 'gender' , 'country' , 'income' , 'like']
    writer = csv.writer(response)

    writer.writerow(fields)

    for record in records:
        profile = record.user
        income = ''

        if profile.income == 1:
            income = '<1000'
        elif profile.income == 2:
            income = '1000~2000'
        elif profile.income == 3:
            income = '2000~2500'
        elif profile.income == 4:
            income = '2500~3000'
        elif profile.income == 5:
            income = '3500~4000'
        elif profile.income == 6:
            income = '>4000'

        gender = 'M'

        if profile.gender == 0:
            gender = 'F'

        writer.writerow([profile.email , str(profile.age) , gender , profile.country , income , record.like])

    return response

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

@login_required
def product_detail_view(request , product_id):
    user = request.user
    company = Company.objects.filter(user = user)

    if not company:
        return redirect('/')

    company = company[0]

    product = get_object_or_404(Product , pk = product_id)

    if request.method == 'POST':
        action = request.POST.get('action' , '')

        if action == 'revoke':
            product.hidden = 1
            product.save()
        elif action == 'recover':
            product.hidden = 0
            product.save()

    records = Record.objects.filter(product = product)

    likes = records.filter(like = 'y')
    dislikes = records.filter(like = 'n')

    male_like = 0
    female_like = 0

    male_dislike = 0
    female_dislike = 0

    less10_like = 0
    b10_15_like = 0
    b15_20_like = 0
    b20_25_like = 0
    b25_30_like = 0
    b30_40_like = 0
    a40_like = 0

    less10_dislike = 0
    b10_15_dislike = 0
    b15_20_dislike = 0
    b20_25_dislike = 0
    b25_30_dislike = 0
    b30_40_dislike = 0
    a40_dislike = 0

    l1000_like = 0
    b1000_2000_like = 0
    b2000_2500_like = 0
    b2500_3000_like = 0
    b3000_3500_like = 0
    b3500_4000_like = 0
    a4000_like = 0

    l1000_dislike = 0
    b1000_2000_dislike = 0
    b2000_2500_dislike = 0
    b2500_3000_dislike = 0
    b3000_3500_dislike = 0
    b3500_4000_dislike = 0
    a4000_dislike = 0

    for like in likes:
        profile = like.user

        if profile.gender == 1:
            male_like += 1
        else:
            female_like += 1

        if profile.age < 10:
            less10_like += 1
        elif profile.age < 15:
            b10_15_like += 1
        elif profile.age < 20:
            b15_20_like += 1
        elif profile.age < 25:
            b20_25_like += 1
        elif profile.age < 30:
            b25_30_like += 1
        elif profile.age < 40:
            b30_40_like += 1
        else:
            a40_like += 1

        if profile.income == 1:
            l1000_like += 1
        elif profile.income == 2:
            b1000_2000_like += 1
        elif profile.income == 3:
            b2000_2500_like += 1
        elif profile.income == 4:
            b2500_3000_like += 1
        elif profile.income == 5:
            b3000_3500_like += 1
        elif profile.income == 6:
            b3500_4000_like += 1
        elif profile.income == 7:
            a4000_like += 1

    for dislike in dislikes:
        profile = dislike.user

        if profile.gender == 1:
            male_dislike += 1
        else:
            female_dislike += 1

        if profile.age < 10:
            less10_dislike += 1
        elif profile.age < 15:
            b10_15_dislike += 1
        elif profile.age < 20:
            b15_20_dislike += 1
        elif profile.age < 25:
            b20_25_dislike += 1
        elif profile.age < 30:
            b25_30_dislike += 1
        elif profile.age < 40:
            b30_40_dislike += 1
        else:
            a40_dislike += 1

        if profile.income == 1:
            l1000_dislike += 1
        elif profile.income == 2:
            b1000_2000_dislike += 1
        elif profile.income == 3:
            b2000_2500_dislike += 1
        elif profile.income == 4:
            b2500_3000_dislike += 1
        elif profile.income == 5:
            b3000_3500_dislike += 1
        elif profile.income == 6:
            b3500_4000_dislike += 1
        elif profile.income == 7:
            a4000_dislike += 1

    return render_to_response("dataapp/product_detail.html", {
        'product': product,
        'company':company,
        'records' : records,
        'likes' : likes.count(),
        'dislikes' : dislikes.count(),
        'male_like' : male_like,
        'male_dislike' : male_dislike,
        'female_like' : female_like,
        'female_dislike' : female_dislike,
        'less10_like' : less10_like,
        'less10_dislike' : less10_dislike,
        'b10_15_like' : b10_15_like,
        'b10_15_dislike' : b10_15_dislike,
        'b15_20_like' : b15_20_like,
        'b15_20_dislike' : b10_15_dislike,
        'b20_25_like' : b20_25_like,
        'b20_25_dislike' : b20_25_dislike,
        'b25_30_like' : b25_30_like,
        'b25_30_dislike' : b25_30_dislike,
        'b30_40_like' : b30_40_like,
        'b30_40_dislike' : b30_40_dislike,
        'a40_like' : a40_like,
        'a40_dislike' : a40_dislike,
        'l1000_like' : l1000_like,
        'l1000_dislike' : l1000_dislike,
        'b1000_2000_like' : b1000_2000_like,
        'b1000_2000_dislike' : b1000_2000_dislike,
        'b2000_2500_like' : b2000_2500_like,
        'b2000_2500_dislike' : b2000_2500_dislike,
        'b2500_3000_like' : b2500_3000_like,
        'b2500_3000_dislike' : b2500_3000_dislike,
        'b3000_3500_like' : b3000_3500_like,
        'b3000_3500_dislike' : b3000_3500_dislike,
        'b3500_4000_like' : b3500_4000_like,
        'b3500_4000_dislike' : b3500_4000_dislike,
        'a4000_like' : a4000_like,
        'a4000_dislike' : a4000_dislike
        }, RequestContext(request))

@login_required
def create_product_view(request):
    user = request.user
    company = Company.objects.filter(user = user)

    if not company:
        return redirect('/')

    company = company[0]

    if request.method == 'POST':
        name = request.POST.get('name' , '')
        startAge = request.POST.get('startAge' , 0)
        endAge = request.POST.get('endAge' , 100)
        gender = request.POST.get('gender' , 3)
        income = request.POST.get('income' , 0)
        country = request.POST.get('country' , 'All')
        image = request.FILES.get('image' , None)

        if image == None:
            return render_to_response("dataapp/create_product.html", {
                'company':company,
                'error':'File not found'
                }, RequestContext(request))

        filename, extension = os.path.splitext(image.name)
        if(extension != '.png' and extension != '.jpg' and extension != '.gif' and extension != '.jpeg'):
            return render_to_response("dataapp/create_product.html", {
                'company':company,
                'error':'File Wrong Type'
                }, RequestContext(request)) 

        DJANGO_TYPE = image.content_type

        if DJANGO_TYPE == 'image/jpeg':
             PIL_TYPE = 'jpeg'
             FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
             PIL_TYPE = 'png'
             FILE_EXTENSION = 'png'

        image = resize_uploaded_image(image)
        temp_handle = StringIO.StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(name)[-1],
                 temp_handle.read(), content_type=DJANGO_TYPE)

        product = Product(company = company, title = name , startAge = startAge , endAge = endAge , targetGender = gender , targetIncome = income , targetCountry = country)
        product.image.save(name + '_' + str(datetime.datetime.now()) + extension , suf, save = False)
        product.save()

        return render_to_response("dataapp/create_product.html", {
            'company':company,
            'success':1
        }, RequestContext(request))

    return render_to_response("dataapp/create_product.html", {
        'company':company
        }, RequestContext(request))