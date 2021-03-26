"""

    enumerators.py

    Enumerators used by our DnD 5e tools

"""

# Sys
from enum import Enum
from enum import IntEnum


class ActionPropertiesEnum(Enum):
    """
    Action Properties
    """

    AMMUNITION = 0  # Ammunition required, also adds Improvised Weapon
    FINESSE = 1  # Can use STR or DEX
    HEAVY = 2  # Small and Tiny take disadvantage
    LIGHT = 3  # Dual Wield!
    LOADING = 4  # Single fire, once per round.
    NO_ADD = 5  # Special type of action, that can't be manually added.
    RANGE = 6  # Bows and the such.
    REACH = 7  # Adds 5ft
    THROWN = 8  # TOSS THAT
    TWOHANDED = 9  # Must be Wielding in both hands.


class ActionTypesEnum(Enum):
    """
    Action Types
    """

    REACTION = 0
    BONUS = 1
    MOVEMENT = 2
    NONE = 3  # Doesn't have an Action Type, for extra effects/abilities.
    STANDARD = 4


class ArmorEnum(IntEnum):
    """
    Armor Enum
    """

    AC_BONUS = 0
    SLOT = 1
    MONSTER_PROPERTIES = 2
    EXTRA = 3


class ArmorSlotsEnum(Enum):
    """
    Armor Slots Enum
    """

    CHEST = 0
    SHIELD = 1


class ClassEnum(Enum):
    """
    Class Enum
    """

    INNATECASTER = 0
    RECHARGE = 1  # Uses the Recharge Mechanic?
    SPELLCASTER = 2


class ConditionTypesEnum(Enum):
    """
    Condition Types
    """

    POISONED = 0


class DamageTypesEnum(Enum):
    """
    Damage Types
    """

    SLASHING = 0
    PIERCING = 1
    FIRE = 10
    RADIANT = 11
    POISON = 12
    COLD = 13
    NECROTIC = 14
    NONE = 99


class EncounterDifficultyXPPerCharacterEnum(IntEnum):
    """
    Encounter Difficulty XP Per Character Enum
    """

    EASY = 0
    MEDIUM = 1
    HARD = 2
    DEADLY = 3


class ExtrasEnum(Enum):
    """
    Extra Enum, used for Extras on Armor/Weapons/Cantrips
    """

    CR_MODIFIER = 0  # How much does this modify our CR?
    DAMAGE_DICE = 1  # Damage Die Range, used when CR Affects Damage Dice
    DEXTERITY_CAP = 2  # Dexterity Mod Cap
    FUNCTION = 3  # Function to call.
    IMPROVISED = 4  # Improvised damage possible?
    RACES_EXEMPT = 5  # Races that can't use this.. thing
    RACES_REQUIRED = 6  # Races that can us this.. thing
    RANGE = 7  # Distance Shot/Thrown
    RECHARGE_TYPE = 8  # Recharge type, from RechargeTypesEnum
    SIZES_EXEMPT = 9  # Sizes that can't use this.. thing.
    SIZES_REQUIRED = 10  # Sizes that can use this.. thing.
    STEALTH_DISADVANTAGE = 11  # Disadvantage on stealth checks
    STRENGTH_REQUIREMENT = 12  # Strength Requirement
    VERSATILE = 13  # For Versatile Damage


class InnateCasterEnum(IntEnum):
    """
    Innatecaster
    """

    STAT = 0
    SPELL_DICT = 1  # Format of Spellname : Times a Day


class MonsterPropertiesEnum(Enum):
    """
    Monster Properties
    """

    BREATH = 0  # Able to use Breath Traits
    BURST = 1  # Able to use Burst Traits
    MARTIAL = 2  # Can use martial weapons/armor/spells
    NATURAL_ARMOR = 3  # Only uses natural armor
    NATURAL_WEAPON = 4  # Only uses claws/bite
    NO_VARIANT_WEAPON = 5  # No Variant Weapons, will equip what is initially
    # given if it meets other properties.
    NO_VARIANT_ARMOR = 6  # No Variant Armor, " "
    NO_VARIANT_SPELL = 7  # No Variant Spells
    NO_VARIANT_INNATE = 8  # No Variant Innate Spells
    SIMPLE = 9  # Only uses simple weapons/armor/spells
    TWOHANDED = 10  # Can use two handed items
    TWOHEADED = 11  # Has two heads


class MonsterStatsByCrEnum(IntEnum):
    """
    Monster Stats By CR Enum
    """

    CR = 0
    PROF_BONUS = 1
    AC = 2
    MIN_HP = 3
    MAX_HP = 4
    ATTACK_BONUS = 5
    DAMAGE_PER_ROUND_MIN = 6
    DAMAGE_PER_ROUND_MAX = 7
    SAVE_DC = 8


class MovementEnum(Enum):
    """
    Movement
    """

    WALK = 0
    FLY = 1
    SWIM = 2


class RaceEnum(Enum):
    """
    Races
    """

    DRAGON = 0
    ELEMENTAL = 1
    GOBLINOID = 2
    HUMANOID = 3
    MONSTROSITY = 4


class RechargeTypeEnum(Enum):
    """
    Recharge Type
    """

    GROUP_LEVEL = 0   # Groups with other Recharges, uses our level


class SenseEnum(Enum):
    """
    Senses Enum
    """

    BLINDSIGHT = 0
    DARKVISION = 1


class SizeEnum(Enum):
    """
    Sizes
    """

    TINY = 4  # d4
    SMALL = 6  # d6
    MEDIUM = 8  # d8
    LARGE = 10  # d10
    HUGE = 12  # d12
    GARGANTUAN = 20  # d20


class SkillsEnum(Enum):
    """
    Skills
    """

    ACROBATICS = 0
    ANIMAL_HANDLING = 1
    ATHLETICS = 2
    ARCANA = 3
    DECEPTION = 4
    HISTORY = 5
    INSIGHT = 6
    INTIMIDATION = 7
    INVESTIGATION = 8
    MEDICINE = 9
    NATURE = 10
    PERCEPTION = 11
    PERFORMANCE = 12
    PERSUASION = 13
    RELIGION = 14
    SLEIGHT_OF_HAND = 15
    STEALTH = 16
    SURVIVAL = 17


class SpecialsEnum(IntEnum):
    """
    Special
    """

    TYPE = 0
    DESCRIPTION = 1
    MONSTER_PROPERTIES = 2
    EXTRA = 3


class SpellCasterEnum(IntEnum):
    """
    Spellcaster
    """

    STAT = 0
    LEVEL = 1
    LIST = 2


class SpellsEnum(IntEnum):
    """
    Spells
    """

    LEVEL = 0
    MONSTER_PROPERTIES = 1
    EXTRA = 2


class StatsEnum(Enum):
    """
    Statsss!
    """

    STRENGTH = 0
    DEXTERITY = 1
    CONSTITUTION = 2
    INTELLIGENCE = 3
    WISDOM = 4
    CHARISMA = 5


class TraitsEnum(IntEnum):
    """
    Traits
    """

    TYPE = 0
    DESCRIPTION = 1
    MONSTER_PROPERTIES = 2
    EXTRA = 3


class WeaponsEnum(IntEnum):
    """
    Weapons Enum
    """

    DAMAGE_TYPE = 0
    DAMAGE_DICE = 1
    ACTION_PROPERTIES = 2
    MONSTER_PROPERTIES = 3
    EXTRA = 4  # Extra string, used for Versatile Damage and Range/Thrown


class WeaponsDictEnum(IntEnum):
    """
    For our Weapons Dict
    """

    NAME = 0
    COUNT = 1
    DICE = 2


# We gotta be included!
if __name__ == '__main__':
    pass
