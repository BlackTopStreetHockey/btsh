from django.urls import include, path
from rest_framework import routers

from .views import TeamSeasonRegistrationViewSet, TeamViewSet


router = routers.SimpleRouter()
router.register(r'teams', TeamViewSet)
router.register(r'team-season-registrations', TeamSeasonRegistrationViewSet)

app_name = 'teams'
urlpatterns = [
    path('', include(router.urls)),
]
