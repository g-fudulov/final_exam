"""
URL configuration for final_exam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('final_exam.easy_drive.urls')),
    path('advertisement/', include("final_exam.easy_drive_ad.urls")),
    path('profile/', include('final_exam.easy_drive_profile.urls')),
    path('blog/', include('final_exam.easy_drive_blog.urls')),
    path("reactions/", include('final_exam.easy_drive_reactions.urls'))
]
