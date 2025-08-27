from django.contrib.auth.models import User

from rest_framework import serializers

from stats.models import (
    Character,
    Stat,

    ResourceType,
    Resource,

    Feature,
    FeatureEffect,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )


class CharacterSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Character
        fields = "__all__"


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = "__all__"


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceType
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class FeatureEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureEffect
        fields = "__all__"
