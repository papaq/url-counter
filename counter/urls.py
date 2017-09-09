from django.conf.urls import url, include

from counter import views

app_name = 'counter'

urlpatterns = [
    url(r'^shorten-url/$', views.shorten_url, name='shorten_url'),
    url(r'^(?P<short_code>\w{5})/history/$', views.history_of_url, name='history_of_url'),
    url(r'^(?P<short_code>\w{5})/history/(?P<redirection_pk>\d+)$', views.redirection_info, name='redirection_info'),
    url(r'^list/$', views.list_url, name='list_url'),
    url(r'^(?P<short_code>\w+)/$', views.redirect_url, name='redirect_url'),
    url(r'^$', views.redirect_to_shorten, name='redirect_to_shorten'),
]
