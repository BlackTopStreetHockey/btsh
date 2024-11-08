from django.urls import include, path
from rest_framework import routers

from .views import SeasonViewSet


router = routers.SimpleRouter()
router.register(r'seasons', SeasonViewSet)

app_name = 'seasons'
urlpatterns = [
    path('', include(router.urls)),
]
