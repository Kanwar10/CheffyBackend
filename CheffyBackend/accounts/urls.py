from django.urls import path

from accounts.api.accounts import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('register/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('sendotp/', SendOtp.as_view()),
    path('validateotp/', ValidateOtp.as_view()),
    path('customer/', CustomerProfileView.as_view()),
    path('partner/',PartnerProfileView.as_view()),
]
