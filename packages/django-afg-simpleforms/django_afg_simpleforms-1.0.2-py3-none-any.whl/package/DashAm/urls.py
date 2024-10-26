"""
URL configuration for DashAm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from package.backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('illustration/', views.illustration, name='illustration'),
    path('engraving/', views.engraving, name='engraving'),
    path('replica/', views.replica, name='replica'),
    path('abstraction/', views.abstraction, name='abstraction'),
    path('interpretation/', views.interpretation, name='interpretation'),
    path('decorative_art/', views.decorative_art, name='decorative_art'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('news/', views.news, name='news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('order_form/', views.order_form, name='order_form'),
    path('order/success/<str:name>/<str:email>/', views.order_success, name='order_success'),
    path('update_views/', views.update_views, name='update_views'),
    path('logout/', LogoutView.as_view(template_name='index.html'), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
