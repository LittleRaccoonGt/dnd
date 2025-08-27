from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from stats.models import (
    Character,
    Stat,

    ResourceType,
    Resource,

    Feature,
    FeatureEffect,
)

from stats.serializers import (
    CharacterSerializer,
    StatSerializer,

    ResourceTypeSerializer,
    ResourceSerializer,

    FeatureSerializer,
    FeatureEffectSerializer,
)


class CharacterViewSet(ModelViewSet):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data)


class StatViewSet(ModelViewSet):
    serializer_class = StatSerializer
    queryset = Stat.objects.all()


class ResourceTypeViewSet(ModelViewSet):
    serializer_class = ResourceTypeSerializer
    queryset = ResourceType.objects.all()


class ResourceViewSet(ModelViewSet):
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()


class FeatureViewSet(ModelViewSet):
    serializer_class = FeatureSerializer
    queryset = Feature.objects.all()


class FeatureEffectViewSet(ModelViewSet):
    serializer_class = FeatureEffectSerializer
    queryset = FeatureEffect.objects.all()

