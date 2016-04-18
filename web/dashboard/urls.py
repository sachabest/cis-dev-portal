from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^github_linker/$', views.link_github, name='github_linker'),
    url(r'^github_handshake/$', views.github_handshake, name='github_handshake'),
    url(r'^jira_linker/$', views.link_jira, name='jira_linker'),
    url(r'^jira_handshake/$', views.jira_handshake, name='jira_handshake'),
    url(r'^uploader/$', views.uploader, name='uploader'),
    url(r'^students/$', views.students, name='students'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^project/(?P<num>[0-9]+)/$', views.project, name='project'),
]