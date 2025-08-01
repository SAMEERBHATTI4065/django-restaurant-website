"""
URL configuration for restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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


# yaha 25 line m include is liya add kiya ku k ham na include ko pyhon m add kiy ha 
# is liya aur ham na include is likha ku k sab se pahle vo restaurat k urls pa a ga 
# vha se core urls.py ki file par chala jay ga aur vha run vgara hoga 


from django.contrib import admin
from django.urls import path, include

# y 31 32 lines m n is liya likhi ta k settings.py url para ha static ka us sa location 
# mila + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) y line darasal
# development testing k liya is ka matlab ha k vo media root aur media url settings 
# m sa la ga 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Your app's urls
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)