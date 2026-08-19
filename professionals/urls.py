from rest_framework.routers import DefaultRouter

from .views import ProfessionalViewSet


router = DefaultRouter()

router.register(
    "",
    ProfessionalViewSet,
    basename="professional",
)

urlpatterns = router.urls