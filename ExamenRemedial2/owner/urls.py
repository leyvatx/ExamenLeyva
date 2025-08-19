from rest_framework import routers
from .views import OwnerViewSet

router = routers.DefaultRouter()
router.register(r'owners', OwnerViewSet)

urlpatterns = router.urls
