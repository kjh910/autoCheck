from django.urls import path, include
from selenium_app import views as views

urlpatterns = [
    path('search/', views.SearchView.as_view(), name='search'),
    path('users/send_email/', views.SendEmail.as_view(), name='send-email'),
    path('users/login/kakao/', views.KakaoLogin.as_view(), name='kakao-login'),
    path('users/login/kakao/callback/', views.KakaoLoginCallback.as_view(), name='kakao-login-callback'),
]