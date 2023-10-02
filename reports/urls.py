from django.urls import path

from reports import views

app_name = "reports"
urlpatterns = [
    path('', views.download_file, name="report"),
]
