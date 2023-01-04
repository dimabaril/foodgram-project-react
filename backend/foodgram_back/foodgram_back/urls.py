from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
# from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path(
    #    'redoc/',
    #    TemplateView.as_view(template_name='redoc.html'),
    #    name='redoc'
    # ),
    path('api/', include('api.urls')),
    path('api/', include('users.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
