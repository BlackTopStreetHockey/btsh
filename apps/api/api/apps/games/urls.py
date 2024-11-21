from django.urls import include, path
from rest_framework import routers

from .views import GameDayViewSet, GameGoalViewSet, GamePlayerViewSet, GameRefereeViewSet, GameViewSet


router = routers.SimpleRouter()
router.register(r'game_days', GameDayViewSet)
router.register(r'games', GameViewSet)
router.register(r'game_referees', GameRefereeViewSet)
router.register(r'game_players', GamePlayerViewSet)
router.register(r'game_goals', GameGoalViewSet)

app_name = 'games'
urlpatterns = [
    path('', include(router.urls)),
]
