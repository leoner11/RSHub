from django.urls import path
from credits_api.views import send_credits_information, retrieve_credits



urlpatterns = [
    path("send_credits_info/", send_credits_information),
    path('retrieve_credits/', retrieve_credits),
]