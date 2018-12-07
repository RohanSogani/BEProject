from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
 # url(r'^$',''), #general pattern
 # url(r'^all/$','appWindow.views.apps'), #to get list of all apps
 # url(r'^get/(?P<app_id>\d+)/$','appWindow.views.app'),#to get app directly from the query box

   	url(r'^upload/',views.upload,name='upload'),
   	url(r'^show_report/(?P<file_name>\w+\.apk)',views.showReport, name='showReport'),
   	url(r'^invalidApp/',views.invalidApp,name='invalidApp'),
   	url(r'^searchReport/', views.searchReport,name='searchReport'),
   	url(r'^allReports/', views.allReports,name='allReports'),
   	url(r'^deleteReports/', views.deleteReports, name='deleteReports'),
    url(r'^index/', views.index,name='index'),
    url(r'^hacksense/', views.hacksense,name='hacksense'),
    url(r'^intellisight/', views.intellisight,name='intellisight'),
    url(r'^appwindow/', views.appwindow,name='appwindow'),
    url(r'^grouppermissions/', views.grouppermissions,name='grouppermissions'),
    url(r'^compare/', views.compare,name='compare'),
    url(r'^team/', views.team,name='team'),
    url(r'^finalComparison/', views.finalComparison,name='finalComparison'),
    
]
