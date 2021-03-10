"""

    settings.py

"""

# Sys
import os

# Moinnnn
from .enumerators import (
    ConditionTypesEnum, DamageTypesEnum,
    MovementEnum, SenseEnum
)

# Base
# ----
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
JSON_DIR = os.path.join(ROOT_DIR, "..", "assets")

# Challenge Ratings
# -----------------
CR = {}

# Condition Immunities CR Mods
CR["CONDITION_IMMUNITIES"] = {
    ConditionTypesEnum.POISONED	:	0.5
}

# Damage Immunities CR Mods
CR["DAMAGE_IMMUNITIES"] = {
    DamageTypesEnum.COLD	:	0.5,
    DamageTypesEnum.POISON	:	0.5
}

# Damage Resists and Vulnerabilities CR Mods
CR["DAMAGE_RESISTANCES"] = {
    DamageTypesEnum.COLD	:	0.25,
    DamageTypesEnum.FIRE	:	0.25,
    DamageTypesEnum.POISON	:	0.25
}
CR["DAMAGE_VULNERABILITIES"] = {}
for key, value in CR["DAMAGE_RESISTANCES"].items():
    CR["DAMAGE_VULNERABILITIES"][key] = value * -1.00

# INNATE CR.
# For INNATE this is PER SPELL LEVEL
CR["INNATECASTING"] = 0.5

# MOVEMENT CR MODS
# The value is per 30ft
CR["MOVEMENT"] = {
    MovementEnum.FLY	:	0.2,
    MovementEnum.WALK	:	0.1
}

# RECHARGE CR
# We take the Recharge Die and subtract it from 7,
# then multiply it by this number
CR["RECHARGE"] = 1.10  # 0.10

# SAVING THROWS CR
CR["SAVING_THROWS"] = 0.25

# SENSES CR, 30ft * CR Adjustment
CR["SENSES"] = {
    SenseEnum.BLINDSIGHT: 0.25,
    SenseEnum.DARKVISION: 0.10
}

# SPELL CR.
# For SPELLS, this is the MAX SPELL LEVEL
CR["SPELLCASTING"] = 0.5

# TRAITS CR
# Traits?
CR["TRAITS"] = 0.05  # 0.25


# We gotta be included!
if __name__ == '__main__':
    pass
