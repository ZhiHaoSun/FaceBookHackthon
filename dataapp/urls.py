from __future__ import absolute_import
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import *
from django.views.generic import CreateView, UpdateView, ListView, RedirectView


urlpatterns = patterns("",
 	url(regex = r'^$', view  = home_view , name = 'home'),
    url(regex = r'^products/', view=login_required(product_list_view) , name="products"),
    url(regex = r'^detail/(?P<product_id>\d*)', view=login_required(product_detail_view) , name="product_detail"),
    url(regex = r'^export/(?P<product_id>\d*)', view=login_required(export_data) , name="export_data"),
    url(regex = r'^create_product/', view=login_required(create_product_view) , name="create_product"),

    url(regex = r'^api/product/', view=product_api , name="product_api"),
    url(regex = r'^api/register/', view=register_api , name="register_api"),
    url(regex = r'^api/post/', view=post_api , name="post_api"),
    url(regex = r'^api/voucher/', view=voucher_api , name="voucher_api"),
)