from django.urls import path

from robots import views

app_name = "robots"
urlpatterns = [
    path('api/', views.APIView, name="api"),
]
