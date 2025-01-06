from django.urls import path

from sbily.users.views import account_views as views

account_urlpatterns = [
    path("me/", views.my_account, name="my_account"),
    path("change_password/", views.change_password, name="change_password"),
    path("resend_verify_email/", views.resend_verify_email, name="resend_verify_email"),
    path("delete/", views.delete_account, name="delete_account"),
]