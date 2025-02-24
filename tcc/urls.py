from django.contrib import admin
from django.urls import path, include
from accounts.urls import urlpatterns as accounts_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include(accounts_urls)),
]
