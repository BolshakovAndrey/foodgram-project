from django.conf import settings
from django.conf.urls import handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = 'recipes.views.page_not_found'  # noqa
handler500 = 'recipes.views.server_error'  # noqa
handler403 = 'recipes.views.permission_denied'  # noqa

urlpatterns = [
    # admin section
    path('admin/', admin.site.urls),
    # registration and authorization
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    # apps
    path('', include('recipes.urls')),
]

urlpatterns += [
    # flatpages
    path("about/about-author/", views.flatpage,
         {"url": "/author/"}, name="about-author"),
    path("about/about-spec/", views.flatpage,
         {"url": "/tech/"}, name="about-tech"),
    path("about/about-site/", views.flatpage,
         {"url": "/site/"}, name="about-site"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
