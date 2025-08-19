from rest_framework import routers
from .views import PlayerViewSet

router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)

urlpatterns = router.urls
