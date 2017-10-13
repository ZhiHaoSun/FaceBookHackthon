from __future__ import absolute_import
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import *
from django.views.generic import CreateView, UpdateView, ListView, RedirectView


urlpatterns = patterns("",
 	url(regex = r'^$', view  = home_view , name = 'home'),
    url(regex = r'^products/', view=login_required(product_list_view) , name="products"),

    url(regex = r'^api/product/', view=product_api , name="product_api"),
    url(regex = r'^api/post/', view=post_api , name="post_api"),
    url(regex = r'^api/voucher/', view=voucher_api , name="voucher_api"),
)