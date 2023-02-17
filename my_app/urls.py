"""my_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('sell/', views.SellView.as_view(), name='sell'),
    path('my_sells/', views.MySellsView.as_view(), name='my_sells'),
    path('edit_sell/<int:pk>/', views.EditSellView.as_view(), name='edit_sell'),
    path('delete_sell/<int:pk>/', views.DeleteSellView.as_view(), name='delete_sell'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
