from django.urls import include, path
from rest_framework import routers

from .views import SeasonRegistrationViewSet, SeasonViewSet


router = routers.SimpleRouter()
router.register(r'seasons', SeasonViewSet)
router.register(r'season-registrations', SeasonRegistrationViewSet)

app_name = 'seasons'
urlpatterns = [
    path('', include(router.urls)),
]
