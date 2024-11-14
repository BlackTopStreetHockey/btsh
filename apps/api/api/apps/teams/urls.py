from django.urls import include, path
from rest_framework import routers

from .views import TeamViewSet, TeamDetailByShortNameView

router = routers.SimpleRouter()
router.register(r'teams', TeamViewSet)

app_name = 'teams'
urlpatterns = [
    path('', include(router.urls)),
    path('team/<str:short_name>/', TeamDetailByShortNameView.as_view(), name='team-by-short-name'),
]
