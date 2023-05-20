from django.urls import path

from . import views

urlpatterns = [
    path("/", views.create_alert, name="create alert"),
    path("/<int:alert_id>", views.delete_alert, name="delete alert"),
    path("/user/<str:user_name>", views.get_all_alerts_for_user, name="get alerts for a user"),
]