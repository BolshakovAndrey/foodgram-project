from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path('', include('recipes.urls')),
    path('about/author/', TemplateView.as_view(
        template_name='about.html'
    ), name='about_author'),
    path('about/tech/', TemplateView.as_view(
        template_name='about.html'
    ), name='about_tech'),
]
