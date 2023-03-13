from django.urls import path, include
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'), 
]
