from django.urls import include, path
from rest_framework import routers

from .views import GameDayViewSet, GamePlayerViewSet, GameRefereeViewSet, GameViewSet


router = routers.SimpleRouter()
router.register(r'game_days', GameDayViewSet)
router.register(r'games', GameViewSet)
router.register(r'game_referees', GameRefereeViewSet)
router.register(r'game_players', GamePlayerViewSet)

app_name = 'games'
urlpatterns = [
    path('', include(router.urls)),
]
