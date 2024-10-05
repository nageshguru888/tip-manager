from django.urls import path
from .views import UserCreateView, LoginView, TipCalculateView, TipListView

urlpatterns = [
    path('user/', UserCreateView.as_view()),
    path('user/login/', LoginView.as_view()),
    path('tip/calculate/', TipCalculateView.as_view()),
    path('tip/', TipListView.as_view()),
]