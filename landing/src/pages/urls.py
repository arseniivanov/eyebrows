# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url, include
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
	#path('', views.index, name='index'),
   # url('detectImage', views.savePhoto), #Specifika URLS ska bort
   # url('detectWithWebcam', views.videoSnap),
    url(r'^api/', include('myapi.urls')),
    url(r'^$', RedirectView.as_view(url='static/index.html', permanent=False), name='index')
     
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)