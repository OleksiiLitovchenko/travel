from rest_framework.routers import DefaultRouter
from .views import TravelProjectViewSet, ProjectPlaceViewSet

router = DefaultRouter()
router.register(r"projects", TravelProjectViewSet, basename="projects")
router.register(r"project-places", ProjectPlaceViewSet, basename="project-places")

urlpatterns = router.urls