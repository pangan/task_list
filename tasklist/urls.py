"""
By Amir Mofakhar <amir@mofakhar.info>
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^task/$', views.task, name='task'),
    url(r'^move/$', views.move_task, name='move'),
    url(r'^delete/$', views.delete_task, name='delete'),

]
