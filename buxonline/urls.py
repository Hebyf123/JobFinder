from django.contrib import admin
from django.urls import path,include
import djoser
import jobs.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('jobs/',include('jobs.urls')),
    path("social_auth/",include('socialauth.urls')),
]
