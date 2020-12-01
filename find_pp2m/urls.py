from django.urls import path
from django.conf.urls import url, include

from . import views

app_name = 'pp2m'
urlpatterns = [
    path('', views.index, name='index'),
    # path('departements/', views.listing_dept, name="listing_dept"),
    path('pp2m_search/<str:cities_name>', views.pp2m_search, name="pp2m_distance"),
    path('pp2m/', views.pp2m_form, name="pp2m_form"),
]
