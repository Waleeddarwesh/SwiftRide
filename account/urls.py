from django.urls import path
from .views import *

urlpatterns=[

    path('register/', RegisterView.as_view(), name='register'),
    path('login/',LoginView.as_view(), name='login'),
    path('user-details/', UserDetailView.as_view(), name='user-details'),
    path('update-user/', UserUpdateView.as_view(), name='update-user'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('set-new-password/', ResetRequestSetNewPasswordView.as_view(), name='set-new-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('delete-account/', UserDeleteView.as_view(), name='delete-account'),
]
    

