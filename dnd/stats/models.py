from django.db import models
from django.contrib.auth.models import User


class Character(models.Model):
    """Base character model"""
    
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="characters",
    )
    name = models.CharField(
        max_length=127,
    )
    level = models.PositiveIntegerField(
        default=1,
    )

    str_val = models.PositiveIntegerField(default=10)
    dex_val = models.PositiveIntegerField(default=10)
    con_val = models.PositiveIntegerField(default=10)
    int_val = models.PositiveIntegerField(default=10)
    wis_val = models.PositiveIntegerField(default=10)
    cha_val = models.PositiveIntegerField(default=10)

    base_hp = models.PositiveIntegerField(default=1)
    base_ac = models.PositiveIntegerField(default=10)
    speed = models.PositiveIntegerField(default=30)


class CharacterClass(models.Model):
    class Name(models.TextChoices):
        BARBARIAN = "barbarian", "Barbarian"
        BARD = "bard", "Bard"
        CLERIC = "cleric", "Cleric"
        DRUID = "druid", "Druid"
        FIGHTER = "fighter", "Fighter"
        MONK = "monk", "Monk"
        PALADIN = "paladin", "Paladin"
        RANGER = "ranger", "Ranger"
        ROGUE = "rogue", "Rogue"
        SORC = "sorcerer", "Sorcerer"
        WARLOCK = "warlock", "Warlock"
        WIZARD  = "wizard", "Wizard"

    character = models.ForeignKey(
        to=Character,
        on_delete=models.CASCADE,
        related_name="classes",
    )
    name = models.CharField(
        max_length=9,
        choices=Name.choices,
    )
    level = models.PositiveIntegerField(
        default=1,
    )

    class Meta:
        unique_together = ("character", "name")


class Stat(models.Model):
    class Key(models.TextChoices):
        AC = "ac"
        MAX_HP = "max_hp"
        INIT = "initiative"
        PROF = "proficiency_bonus"
    
    character = models.ForeignKey(
        to=Character,
        on_delete=models.CASCADE,
        related_name="stats",
    )
    key = models.CharField(
        max_length=64,
        choices=Key.choices,
    )
    base_value = models.IntegerField(
        default=0,
    )

    class Meta:
        unique_together = ("character", "key")
    

class ResourceType(models.Model):
    class Recovery(models.TextChoices):
        SHORT = "short_rest"
        LONG = "long_rest"
        DAILY = "daily"

    key = models.CharField(
        max_length=64,
        unique=True
    )
    name = models.CharField(
        max_length=127,
    )
    max_formula = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )
    recovery = models.CharField(
        max_length=32,
        choices=Recovery.choices,
    )


class Resource(models.Model):
    character = models.ForeignKey(
        to=Character,
        on_delete=models.CASCADE,
        related_name="resources",
    )
    resource_type = models.ForeignKey(
        to=ResourceType,
        on_delete=models.CASCADE,
        related_name="+",
    )
    current = models.IntegerField(
        default=0,
    )
    

class Feature(models.Model):
    class Source(models.TextChoices):
        RACE = "race"
        CLASS = "class"
        ITEM = "item"
        SPELL = "spell"
        FEAT = "feat"
        MISC = "misc"
    
    character = models.ForeignKey(
        to=Character,
        on_delete=models.CASCADE,
        related_name="features",
    )
    name = models.CharField(
        max_length=127,
    )
    source = models.CharField(
        max_length=16,
        choices=Source.choices,
    )


class FeatureEffect(models.Model):
    class TargetType(models.TextChoices):
        STAT = "stat"
        MAX = "resource_max"
        FLAG = "flag"
    
    class Operation(models.TextChoices):
        ADD = "add"
        SUB = "sub"
        MUL = "mul"
        DIV = "div"
        SET = "set"
        TOGGLE = "toggle"
    
    class ValueKind(models.TextChoices):
        CONST = "const"
        REF = "reference"
        FORMULA = "formula"
    
    feature = models.ForeignKey(
        to=Feature,
        on_delete=models.CASCADE,
        related_name="effects",
    )
    target_type = models.CharField(
        max_length=16,
        choices=TargetType.choices,
    )
    target_key = models.CharField(
        max_length=64,
    )
    operation = models.CharField(
        max_length=8,
        choices=Operation.choices,
    )
    value_kind = models.CharField(
        max_length=12,
        choices=ValueKind.choices,
    )
    value_str = models.CharField(
        max_length=255,
    )
    enabled = models.BooleanField(
        default=True,
    )
