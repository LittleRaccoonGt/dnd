from django.urls import path, include

from rest_framework.routers import DefaultRouter

from stats.views import (
    CharacterViewSet,
    StatViewSet,

    ResourceTypeViewSet,
    ResourceViewSet,

    FeatureViewSet,
    FeatureEffectViewSet,
)


router = DefaultRouter()

router.register(r"characters", CharacterViewSet, basename="characters")
router.register(r"stats", StatViewSet, basename="stats")

router.register(r"resource-types", ResourceTypeViewSet, basename="resource-types")
router.register(r"resources", ResourceViewSet, basename="resources")

router.register(r"features", FeatureViewSet, basename="features")
router.register(r"feature-effects", FeatureEffectViewSet, basename="feature-effects")


urlpatterns = [
    path("v1/", include(router.urls)),
]
