from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("apply/", views.application_view, name="apply"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("applications/<int:application_id>/documents/<str:field_name>/", views.application_document, name="application_document"),
]
