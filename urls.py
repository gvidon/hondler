# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from views                     import *


urlpatterns = patterns('',
	url(r'^add/(?P<pk>\d+)/?$'   , add     , name='add'),
	url(r'^checkout/?$'          , checkout, name='checkout'),
	url(r'^items/?$'             , items   , name='items'),
	url(r'^order/?$'             , order   , name='order'),
	url(r'^remove/(?P<pk>\d+)/?$', remove  , name='remove'),
	url(r'^update/?$'            , update  , name='update'),
)
