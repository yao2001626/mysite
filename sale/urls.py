from django.conf.urls import patterns, url
from django.contrib import admin

from .views import Hello

admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^(\w+)/$', Hello.as_view(), name='weixin_entry'),
)