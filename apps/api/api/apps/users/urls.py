from django.urls import include, path
from rest_framework import routers

from .views import UserSeasonRegistrationViewSet


router = routers.SimpleRouter()
router.register(r'user-season-registrations', UserSeasonRegistrationViewSet)

app_name = 'users'
urlpatterns = [
    path('', include(router.urls)),
]
