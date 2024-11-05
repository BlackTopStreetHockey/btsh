from django.urls import include, path
from rest_framework import routers

from .views import DivisionViewSet


router = routers.SimpleRouter()
router.register(r'divisions', DivisionViewSet)

app_name = 'divisions'
urlpatterns = [
    path('', include(router.urls)),
]
