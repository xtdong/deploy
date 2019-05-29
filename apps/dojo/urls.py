from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.display_book_list),
    url(r'^books/add$', views.display_add_book),
    url(r'^books/process_add_book$', views.process_add_book),
    url(r'^books/(?P<book_id>\d+)$', views.display_book),
    url(r'^add_review$', views.add_review),
    url(r'^delete_review', views.delete_review),
    url(r'^users/(?P<user_id>\d+)$', views.display_user)
]
