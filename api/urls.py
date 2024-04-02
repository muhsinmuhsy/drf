from django.urls import path
from api.views import *

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    # path('current_user/', CurrentUser.as_view(), name='current_user'),
]