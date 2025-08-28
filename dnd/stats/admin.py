from django.contrib import admin

from stats.models import (
    Character,
    CharacterClass,
    Stat,
    
    ResourceType,
    Resource,

    Feature,
    FeatureEffect,
)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin): ...

@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin): ...

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin): ...

@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin): ...

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin): ...

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin): ...

@admin.register(FeatureEffect)
class FeatureEffectAdmin(admin.ModelAdmin): ...
