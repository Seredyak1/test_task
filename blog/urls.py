from rest_framework import routers

from .views import PostAPIView


router = routers.SimpleRouter()
router.register('', PostAPIView)
urlpatterns = router.urls
