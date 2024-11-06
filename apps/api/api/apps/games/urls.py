from django.urls import include, path
from rest_framework import routers

from .views import GameDayViewSet


router = routers.SimpleRouter()
router.register(r'game_days', GameDayViewSet)

app_name = 'game_days'
urlpatterns = [
    path('', include(router.urls)),
]
