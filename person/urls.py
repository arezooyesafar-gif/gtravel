from django.urls import path, include

from visa.utils import visa_pdf
from .views import *
from .ajax_view import *

urlpatterns = [
    path('ajax_user_list', ajax_user_list, name='ajax_user_list'),
    path('', LoginPage, name='login'),
    path('logout', LogoutPage, name='logout'),
    path('user_list', user_list, name='user_list'),
    path('delete_user/<int:id>', delete_user, name='delete_user'),
    path('my_profile/<int:id>', user_profile, name='user_profile'),
    path('user_profile_update/<int:id>', user_profile_update, name='user_profile_update'),
    path('reset_password_admin/<int:id>', reset_password_admin, name='reset_password_admin'),
    # path('user_varify_number/<int:prf_id>/<int:id>', otp_varify, name='otp_varify'),
    #visa urls
    path('otp_login', otp_login, name='otp_login'),
    path('varify_otp_login/<int:id>', varify_otp_login, name='varify_otp_login'),
    path('register', create_user, name='create_user'),
    path('varify_otp/<int:id>', varify_otp, name='varify_otp'),
    path('visa_panel/<int:id>', visa_panel, name='visa_panel'),
    path('logout', LogoutPage, name='logout'),
    path('profile', profile_view, name='profile_view'),
    path('applications', visa_list, name='visa_list'),
    path('applications_list', visa_list_admin, name='visa_list_admin'),
    path('update_visa_request/<int:id>', update_visa_request, name='update_visa_request'),
    path('visa_view/<int:id>', visa_view, name='visa_view'),
    path('visa_pdf/<int:id>', visa_pdf, name='visa_pdf'),
    path('delete_visa/<int:id>', delete_visa_request, name='delete_visa_request'),
    path('delete_thai_visa/<int:id>', delete_thai_visa_request, name="delete_thai_visa_request"),
    path('thai/applications', thai_visa_list, name='thai_visa_list'),
    path('thai/update_visa_request/<int:id>', update_thai_visa_request, name='update_thai_visa_request'),
    path('thai/visa_panel/<int:id>', thai_visa_panel, name='thai_visa_panel'),
    path('visa/select-country/<int:id>', visa_country, name='visa_country'),
]