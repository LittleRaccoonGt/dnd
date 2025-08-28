import math
import logging

from typing import Any
from dataclasses import dataclass

from stats.models import Character, FeatureEffect


logger = logging.getLogger(__name__)


SAVE_FUNCTIONS = {
    "abs": abs,
    "min": min,
    "max": max,
    "round": round,
    "ceil": math.ceil,
    "floor": math.floor,
}


def save_eval(expression: str, context: dict[str, Any]) -> Any:
    allowed = {**SAVE_FUNCTIONS, **context}
    code = compile(expression, "<formula>", "eval")

    for name in code.co_names:
        if name not in allowed:
            raise ValueError(f"Unknown symbol in formula: {name}")
    
    return eval(code, {"__builtins__": {}}, allowed)


@dataclass
class StatBlock:
    stats: dict[str, int]
    flags: dict[str, bool]
    resources_max: dict[str, int]

    def add(self, key, value):
        self.stats[key] = self.stats.get(key, 0) + value

    def sub(self, key, value):
        self.stats[key] = self.stats.get(key, 0) - value

    def mul(self, key, value):
        self.stats[key] = self.stats.get(key, 0) * value

    def div(self, key, value):
        self.stats[key] = self.stats.get(key, 0) // value

    def set(self, key, value):
        self.stats[key] = value

    def set_flag(self, key, value):
        self.stats[key] = bool(value)

    def add_max(self, key, value):
        self.resources_max[key] = self.resources_max.get(key, 0) + value

    def sub_max(self, key, value):
        self.resources_max[key] = self.resources_max.get(key, 0) - value

    def mul_max(self, key, value):
        self.resources_max[key] = self.resources_max.get(key, 0) * value

    def div_max(self, key, value):
        self.resources_max[key] = self.resources_max.get(key, 0) // value

    def set_max(self, key, value):
        self.resources_max[key] = value


def ability_modification(value: int) -> int:
    return (value - 10) // 2


def build_context(character: Character) -> dict[str, Any]:
    class_levels = {c.name: c.level for c in character.classes.all()}
    total_level = sum(class_levels.values())

    proficiency_bonus = 2 + (max(total_level, 1) - 1) // 4

    context = {
        "level": total_level,
        "proficiency_bonus": proficiency_bonus,

        "str_val": character.str_val,
        "dex_val": character.dex_val,
        "con_val": character.con_val,
        "int_val": character.int_val,
        "wis_val": character.wis_val,
        "cha_val": character.cha_val,

        "str_mod": ability_modification(character.str_val),
        "dex_mod": ability_modification(character.dex_val),
        "con_mod": ability_modification(character.con_val),
        "int_mod": ability_modification(character.int_val),
        "wis_mod": ability_modification(character.wis_val),
        "cha_mod": ability_modification(character.cha_val),

        "base_hp": character.base_hp,
        "base_ac": character.base_ac,
        "speed": character.speed,
    }

    for name, level in class_levels.items():
        context[f"{name}_level"] = level
    
    return context


def value_from(effect: FeatureEffect, context: dict[str, Any]) -> Any:

    if effect.value_kind == "const":
        value = effect.value_str.strip().lower()
        
        if value in ("true", "false"):
            return value == "true"

        return effect.value_str
    
    if effect.value_kind == "ref":
        return context.get(effect.value_str)
    
    if effect.value_kind == "formula":
        return save_eval(effect.value_str, context)
    
    raise ValueError(f"Unknown value kind: {effect.value_kind}")


def compute_character_list(character: Character):

    def apply(effect: FeatureEffect):
        """"""
        if not effect.enabled:
            return
        value = value_from(effect, context)

        if effect.target_type == "stat":
            if effect.operation == "add": stat_block.add(effect.target_key, value)
            elif effect.operation == "sub": stat_block.sub(effect.target_key, value)
            elif effect.operation == "mul": stat_block.mul(effect.target_key, value)
            elif effect.operation == "div": stat_block.div(effect.target_key, value)
            else: stat_block.set(effect.target_key, value)
        
        elif effect.target_type == "flag":
            if effect.operation == "toggle": stat_block.set_flag(effect.target_key, value)
            else: stat_block.set_flag(effect.target_key, bool(value))
        
        elif effect.target_type == "resource_max":
            if effect.operation == "add": stat_block.add_max(effect.target_key, value)
            elif effect.operation == "sub": stat_block.sub_max(effect.target_key, value)
            elif effect.operation == "mul": stat_block.mul_max(effect.target_key, value)
            elif effect.operation == "div": stat_block.div_max(effect.target_key, value)
            else: stat_block.set_max(effect.target_key, value)
        

    context = build_context(character)

    stat_block = StatBlock(
        stats={stat.key: int(stat.base_value) for stat in character.stats.all()},
        flags={},
        resources_max={},
    )

    for resource in character.resources.select_related("resource_type").all():
        resource_type = resource.resource_type
        if resource_type.max_formula:
            value = save_eval(resource_type.max_formula, context)
        else:
            value = 0
        stat_block.set_max(resource_type.key, int(value))

    for feature in character.features.prefetch_related("effects").all():
        for effect in feature.effects.all():
            apply(effect)
    
    return {
        "base": context,
        "stats": stat_block.stats,
        "flags": stat_block.flags,
        "resources": {
            resource.resource_type.hey: {
                "current": resource.current,
                "max": int(stat_block.resources_max.get(
                    resource.resource_type.key, 0
                ))
            }
            for resource in character.resources.select_related("resource_type")
        }
    }
