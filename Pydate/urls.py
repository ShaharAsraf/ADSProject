"""Pydate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from Pydate import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base, ),
    path('register/', views.register),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('add_personal_questions/', views.add_personal_questions),
    path('chat/', include('Chat.urls')),
    path('profile/', views.profile),
    path('info/', views.info_view, name='info'),
    path('profile/edit/', views.update_profile),
    path('profile/editimg/', views.update_profile_picture),
    path('my_matches/', views.my_matches, name="my_matches"),
    path('view_people/', views.view_people, name="view_people"),
    path('remind_pass/', views.remind_pass, name="remind_pass"),
    url(r'^view_people/(?P<user_id>\d+)/make_crush$', views.yes_crush, name='yes_crush'),
    url(r'^view_people/(?P<user_id>\d+)/decline_crush$', views.no_crush, name='no_crush'),
    url(r'^logout/$', views.logout_view, name='logout')
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
