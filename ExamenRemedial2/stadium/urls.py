from rest_framework import routers
from .views import StadiumViewSet

router = routers.DefaultRouter()
router.register(r'stadiums', StadiumViewSet)

urlpatterns = router.urls
