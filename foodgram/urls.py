import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import handler404, handler500, handler403

handler404 = "recipes.views.page_not_found" # noqa
handler500 = "recipes.views.server_error" # noqa
handler403 = "recipes.views.permission_denied" # noqa

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
    path('', include("recipes.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
