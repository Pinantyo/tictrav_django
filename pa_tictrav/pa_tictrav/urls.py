from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

from tictrav import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tictrav.urls')), # TicTrav
    path('chatbot/',include('chatbot.urls')), # App chatbot
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Custom URL Error
handler404 = views.handler404
handler500 = views.handler500
handler403 = views.handler403