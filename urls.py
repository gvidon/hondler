# -*- coding: utf-8 -*-
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.defaults       import *
from django.views.generic.base       import TemplateView
from django.contrib                  import admin
from django.conf                     import settings
from views                           import *


urlpatterns = patterns('',
	url(r'^add/(?P<pk>\d+)/?$'   , add                                                , name='add'),
	url(r'^checkout/?$'          , checkout                                           , name='checkout'),
	url(r'^confirmed/?$'         , TemplateView.as_view(template_name='thankyou.html'), name='thankyou'),
	url(r'^items/?$'             , items                                              , name='items'),
	url(r'^order/?$'             , order                                              , name='order'),
	url(r'^remove/(?P<pk>\d+)/?$', remove                                             , name='remove'),
	url(r'^update/?$'            , update                                             , name='update'),
)
