from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^github_linker/$', views.link_github, name='github_linker'),
    url(r'^github_handshake/$', views.github_handshake, name='github_handshake')

]