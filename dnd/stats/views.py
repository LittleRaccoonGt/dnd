from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse

from stats.calculator import compute_character_list

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

    CharacterSheetSerializer,
)


@extend_schema_view(
    sheet=extend_schema(
        responses={200: OpenApiResponse(CharacterSheetSerializer)}
    )
)
class CharacterViewSet(ModelViewSet):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"])
    def sheet(self, request, pk=None):
        character = self.get_object()
        character_sheet = compute_character_list(character)
        return Response(CharacterSheetSerializer(character_sheet).data)


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

