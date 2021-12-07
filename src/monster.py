"""

    Monster.py

    That which is a monster.  Including stats, loot, and description?

"""

# Sys
import math
import statistics

# Emperts
from .armors import Armors
from .challengerating import (
    cr_defense, cr_offense, get_cr_from_row,
    get_monster_stats_from_cr, get_xp_by_cr
)
from .TbTBalancedStats.src.balancedstats import BalancedStats
from .enumerators import ActionPropertiesEnum, ActionTypesEnum, ClassEnum,  ExtrasEnum, InnateCasterEnum, MonsterStatsByCrEnum, MovementEnum, RechargeTypeEnum, SkillsEnum, SpecialsEnum, SpellCasterEnum, SpellsEnum, StatsEnum, TraitsEnum
from .ext.dice import Dice
from .settings import *
from .spells import Spells
from .universals import (
    get_json_data, number_signed, range_dict_from_list,
    spaced_list, number_ord
)
from .weapons import Weapons


__all__ = ["Monster", "MonsterWrapper"]


# ARMOR
ARMOR = get_json_data("armor")

# Dashes
DASHES = "-" * 50

# For Innate
# We store spells in the level based upon how many casts per day they have
# We have Cantrips and then 9 spell slots.
INNATE_SPELLS_PER_LEVEL = [	9] * 10

# Loot.  CP Range first.  Then d100 Roll Ranges.
# Then Values in CP, SP, EP, GP, and PP.
LOOT = range_dict_from_list([
    [0, 4, range_dict_from_list([
        [0, 	29, [Dice(6, 5), None, 			None, 			None, 			None]],
        [30, 	59, [None, 		Dice(6, 4), 	None, 			None, 			None]],
        [60, 	69, [None, 		None, 			Dice(6, 3), 	None, 			None]],
        [70, 	94, [None, 		None, 			None, 			Dice(6, 3), 	None]],
        [95, 	99, [None, 		None, 			None, 			None, 			Dice(6, 1)]]
       ]
    )],
    [5, 10, range_dict_from_list([
        [0, 	29, [Dice(6, 400), 	None, 			None, 			None, 			None]],
        [30,	59,	[None, 			Dice(6, 60),	None, 			Dice(6, 20), 	None]],
        [60, 	69, [None, 			None, 			Dice(6, 30), 	Dice(6, 20), 	None]],
        [70, 	94,	[None, 			None, 			None, 			Dice(6, 40), 	None]],
        [95,	99, [None, 			None, 			None, 			Dice(6, 20), 	Dice(6, 3)]]
       ]
    )],
    [11, 16, range_dict_from_list([
        [0,  19, [None, Dice(6, 400), 	None, 			Dice(6, 100), None]],
        [20, 34, [None, None, 			Dice(6, 100), Dice(6, 100), None]],
        [35, 74, [None, None, 			None, 			Dice(6, 200), Dice(6, 10)]],
        [75, 99, [None, None, 			None, 			Dice(6, 200), Dice(6, 20)]]
       ]
    )],
    [17, 99, range_dict_from_list([
        [0, 14, 	[None, None, Dice(6, 2000), 	Dice(6, 800), 	None]],
        [15, 54, 	[None, None, None, 			Dice(6, 1000), 	Dice(6, 100)]],
        [55, 99, 	[None, None, None, 			Dice(6, 1000), 	Dice(6, 200)]]
       ]
    )]
])

# SKILLS
SKILLS = {
    StatsEnum.STRENGTH		: [SkillsEnum.ATHLETICS],
    StatsEnum.INTELLIGENCE	: [
        SkillsEnum.ARCANA, SkillsEnum.INVESTIGATION,
        SkillsEnum.NATURE, SkillsEnum.RELIGION, SkillsEnum.HISTORY
    ],
    StatsEnum.DEXTERITY		: [
        SkillsEnum.STEALTH, SkillsEnum.SLEIGHT_OF_HAND,
        SkillsEnum.ACROBATICS
    ],
    StatsEnum.CHARISMA		: [
        SkillsEnum.PERFORMANCE, SkillsEnum.DECEPTION,
        SkillsEnum.INTIMIDATION, SkillsEnum.PERSUASION
    ],
    StatsEnum.WISDOM		: [
        SkillsEnum.INSIGHT, SkillsEnum.ANIMAL_HANDLING,
        SkillsEnum.MEDICINE, SkillsEnum.SURVIVAL, SkillsEnum.PERCEPTION
    ]
}

# SPECIALS
# They come with their own ExtraEnum.Func to dictate if they are in play.
SPECIALS = get_json_data("special")

# SPELLS
SPELLS = get_json_data("spells")

# Spells by Spellcaster Level
# LEVEL -> Cantrips, 1st, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, 9th
SPELLS_BY_LEVEL = {
    0	:	[	3, 	0,	0,	0,	0,	0,	0,	0,	0,	0	],
    1	:	[	3,	2,	0,	0,	0,	0,	0,	0,	0,	0	],
    2	:	[	3,	3,	0,	0,	0,	0,	0,	0,	0,	0	],
    3	:	[	3,	4,	2,	0,	0,	0,	0,	0,	0,	0	],
    4	:	[	4,	4,	3,	0,	0,	0,	0,	0,	0,	0	],
    5	:	[	4,	4,	3,	2,	0,	0,	0,	0,	0,	0	],
    6	:	[	4,	4,	3,	3,	0,	0,	0,	0,	0,	0	],
    7	:	[	4,	4,	3,	3,	1,	0,	0,	0,	0,	0	],
    8	:	[	4,	4,	3,	3,	2,	0,	0,	0,	0,	0	],
    9	:	[	4,	4,	3,	3,	3,	1,	0,	0,	0,	0	],
    10	:	[	5,	4,	3,	3,	3,	2,	0,	0,	0,	0	],
    11	:	[	5,	4,	3,	3,	3,	2,	1,	0,	0,	0	],
    12	:	[	5,	4,	3,	3,	3,	2,	1,	0,	0,	0	],
    13	:	[	5,	4,	3,	3,	3,	2,	1,	1,	0,	0	],
    14	:	[	5,	4,	3,	3,	3,	2,	1,	1,	0,	0	],
    15	:	[	5,	4,	3,	3,	3,	2,	1,	1,	1,	0	],
    16	:	[	5,	4,	3,	3,	3,	2,	1,	1,	1,	0	],
    17	:	[	5,	4,	3,	3,	3,	2,	1,	1,	1,	1	],
    18	:	[	5,	4,	3,	3,	3,	3,	1,	1,	1,	1	],
    19	:	[	5,	4,	3,	3,	3,	3,	2,	1,	1,	1	],
    20	:	[	5,	4,	3,	3,	3,	3,	2,	2,	1,	1	]
}

# Traits are Actions that usually have special triggers
# and can cost different things to use.
TRAITS = get_json_data("traits")

# WEAPONS
# NAME, DAMAGE TYPE, DAMAGE DICE, PROPERTIES, EXTRA
WEAPONS = get_json_data("weapons")


class Monster:
    """
    That which we must fight.. or friend... or.. uhm... I dunno... hang out
    with at a bar?
    Name, Size, Race, Alignment, # Hit Dice, Expected CR, Attacks Per Round,
    Movements, Class, Stats [STR, CON, DEX, INT, WIS, CHA], Skill Bonuses,
    Senses, Languages, Traits, Weapons, Armor, MonsterProperties, DVuls,
    DRes, DImm, CImm
    """

    def __init__(
                self, name, size, race, alignment, hit_dice_count, expected_cr,
                attacks_per_round, movement_dict, class_dict, stat_list,
                saving_throws_list, skill_bonus_dict, senses_dict,
                languages_list, traits_list, weapon_list, armor_list,
                monster_properties_list, damage_resistances_list,
                damage_vulnerabilities_list, damage_immunities_list,
                condition_immunities_list
               ):
        """
        Constructor!
        """

        self._name = name
        self._size = size
        self._race = race
        self._alignment = alignment
        self._hit_dice = Dice(size.value, hit_dice_count)
        self._expected_cr = expected_cr
        self._attacks_per_round = attacks_per_round
        self._class_dict = class_dict

        # Resists/Vulnerabilities/Immunities
        self._damage_resistances_list = damage_resistances_list
        self._damage_vulnerabilities_list = damage_vulnerabilities_list
        self._damage_immunities_list = damage_immunities_list
        self._condition_immunities_list = condition_immunities_list

        # Set our Stats
        self._stats = BalancedStats(stats=stat_list, extra_points=0, maximum_stat=30)

        # Lists and Dicts Initializers
        self._armors = Armors(self._stats, ARMOR)
        self._languages_list = []
        self._monster_properties_list = []
        self._movement_dict = {}
        self._senses_dict = {}
        self._saving_throws_list = []
        self._skill_bonus_dict = {}
        self._traits_list = []
        self._weapons = Weapons(
            self._stats, self.get_prof_bonus(),
            self._size, WEAPONS
        )

        # Calculates our HP Average
        self._hp = self.get_hp_average()

        # Monster Properties
        # Done here because Armor/Weapon/Spells/Traits use these
        # to see if we can use them.
        for i in range(0, len(monster_properties_list)):
            self.add_monster_property(monster_properties_list[i])

        # Are we a Caster Class, if so, build our Spells.
        self.setup_spells()

        # Are we an innate spellcaster?
        self.setup_innate()

        # Armor List
        for i in range(0, len(armor_list)):
            self.add_armor(armor_list[i])

        # Languages List
        for i in range(0, len(languages_list)):
            self.add_language(languages_list[i])

        # Movement Dict
        for key, value in movement_dict.items():
            self.add_movement(key, value)

        # SAVING_THROWS List
        for i in range(0, len(saving_throws_list)):
            self.add_saving_throw(saving_throws_list[i])

        # Senses Dict
        for key, value in senses_dict.items():
            self.add_sense(key, value)

        # Skill Bonus List
        for key, value in skill_bonus_dict.items():
            self.add_skill(key, value)

        # Due to Passives, we then add these Skills as 0s.
        # If we already have the skill it'll do nothing.
        self.add_skill(SkillsEnum.PERCEPTION, 0)
        self.add_skill(SkillsEnum.INSIGHT, 0)
        self.add_skill(SkillsEnum.INVESTIGATION, 0)

        # Traits List
        for i in range(0, len(traits_list)):
            self.add_trait(traits_list[i])

        # Weapon List
        for i in range(0, len(weapon_list)):
            self.add_weapon(weapon_list[i])

    def add_armor(self, compound):
        """
        Add some Armor
        """

        # Create the armor
        armor = self._armors.create(compound)

        # Don't already have this armor?
        if self._armors.has_armor(armor):
            return False

        # Can we even use it?
        if not self.can_has_property(armor.get_monster_properties()):
            return False

        # Need to make sure we don't already have this slot taken up.
        if self._armors.has_slot_by_armor(armor):
            return False

        # Now.  Does this armor have a STR requirement?
        if (
            armor.has_extra(ExtrasEnum.STRENGTH_REQUIREMENT) and
            armor.get_extra(ExtrasEnum.STRENGTH_REQUIREMENT) >
            self._stats.get_stat(StatsEnum.STRENGTH)
        ):
            return False

        # Add it!
        self._armors.add(armor)

    def add_language(self, language):
        """
        Add a Language
        """

        if language not in self._languages_list:
            self._languages_list.append(language)

    def add_monster_property(self, monster_property):
        """
        Add Monster Property
        """

        if monster_property not in self._monster_properties_list:
            self._monster_properties_list.append(monster_property)

    def add_movement(self, movement_name, movement_value):
        """
        Add a Movement
        """

        if movement_name not in self._movement_dict:
            self._movement_dict[movement_name] = movement_value

    def add_saving_throw(self, saving_throw):
        """
        Adds a Saving Throw
        """

        if saving_throw not in self._saving_throws_list:
            self._saving_throws_list.append(saving_throw)

    def add_sense(self, sense_name, sense_value):
        """
        Add a Sense!
        """

        if sense_name not in self._senses_dict:
            self._senses_dict[sense_name] = sense_value

    def add_skill(self, skill_name, skill_value):
        """
        Add Skill
        """

        if skill_name not in self._skill_bonus_dict:
            self._skill_bonus_dict[skill_name] = skill_value

    def add_spell(self, spell, spell_level, instance):
        """
        Add Spell
        """

        # Can we use this spell?
        if self.can_has_property(SPELLS[spell][SpellsEnum.MONSTER_PROPERTIES]):
            instance.add(spell, spell_level)

    def add_trait(self, trait):
        """
        Add a Trait
        """

        # Have this trait?
        if trait in self._traits_list:
            return False

        # Can use?
        if not self.can_has_property(
            TRAITS[trait][TraitsEnum.MONSTER_PROPERTIES]
        ):
            return False

        # Does this trait have Size/Race Stuffs?
        if not self.is_extra_size_or_race(TRAITS[trait][TraitsEnum.EXTRA]):
            return False

        # Add
        self._traits_list.append(trait)
        self._traits_list.sort()

    def add_weapon(self, compound):
        """
        Add a Weapon
        """

        # Weapon
        weapon = self._weapons.create(compound)

        # This a NO_ADD?
        if weapon.has_action_property(ActionPropertiesEnum.NO_ADD):
            return False

        # Can equip?
        if not self.can_has_property(weapon.get_monster_properties()):
            return False

        # Only allow three weapons?
        if self._weapons.count() >= 3:
            return False

        # Is this weapon a RANGE weapon?  If so, only take one.
        if (
            weapon.has_action_property(ActionPropertiesEnum.RANGE) and
            self._weapons.get_property_count(ActionPropertiesEnum.RANGE)
        ):
            return False

        # How many of this weapon do we already have?  If we have two and
        # this isn't a THROWN weapon, don't take another.
        if (
            self._weapons.count(weapon.get_name()) and
            not weapon.has_action_property(ActionPropertiesEnum.THROWN)
        ):
            return False

        # Add!
        self._weapons.add(weapon)

    def can_has_property(self, monster_properties):
        """
        We Has Monster Property?
        """

        for monster_property in monster_properties:
            if not self.has_monster_property(monster_property):
                return False
        return True

    def get_armor_disadvantage_on_stealth_string(self):
        """
        Gets the armor we are wearing that has the Sneak Penalty
        """

        # Look through our armor for DISADVANTAGE ON STEALTH
        armor = self._armors.get_extra(ExtrasEnum.STEALTH_DISADVANTAGE)

        # Exists?
        if armor:
            return armor.get_name() + " ARMOR"

        # Must have been mistaken, don't have that effect on us.
        return ""

    def get_cr(self):
        """
        Calculates Challenge Rating
        """

        # Set up cr settings values, those we tweak.
        cr_settings = {}
        cr_settings["CONDITION_IMMUNITIES"] = 0
        cr_settings["DAMAGE_IMMUNITIES"] = 0
        cr_settings["DAMAGE_RESISTANCES"] = 0
        cr_settings["DAMAGE_VULNERABILITIES"] = 0
        cr_settings["INNATECASTING"] = 0
        cr_settings["MOVEMENT"] = 0
        cr_settings["RECHARGE"] = 0
        cr_settings["SAVING_THROWS"] = 0
        cr_settings["SENSES"] = 0
        cr_settings["SPELLCASTING"] = 0
        cr_settings["TRAITS"] = 0

        # We take these seperate because we need to average them and
        # not include them in the total.
        cr_base = {}
        cr_base["DEFENSE"] = self.get_cr_defense()
        cr_base["OFFENSE"] = self.get_cr_offense()

        # Check Traits
        # If they have a CR_MODIFIER, add it.
        for trait in self._traits_list:

            # CR Modifier
            cr_settings["TRAITS"] += (
                self.get_extra_trait(ExtrasEnum.CR_MODIFIER) * CR["TRAITS"]
            )

            # Recharge?
            cr_settings["RECHARGE"] += (
                self.get_recharge_die_calculation() *
                CR["RECHARGE"]
            )

        # Movements
        for movement in self._movement_dict.keys():

            # This a value we check against?
            if movement in CR["MOVEMENT"].keys():

                # Divide!
                thirty_feet_count = self._movement_dict[movement] / 30

                # Modify CR
                cr_settings["MOVEMENT"] += (
                    CR["MOVEMENT"][movement] * thirty_feet_count
                )

        # Innate Spellcasting
        # With Innate, we take the combined level of the Spells
        # And multiply it by our SPELLCASTING_CR
        if self.is_innate_caster():

            # Get our spellss
            for spell in self.innate.get_spells_single_list():
                cr_settings["INNATECASTING"] += (
                    SPELLS[spell][SpellsEnum.LEVEL] * CR["INNATECASTING"]
                )

        # Spellcasting
        # Works off of the highest level of spell castable.
        if self.is_spell_caster():
            cr_settings["SPELLCASTING"] = (
                self._spells.get_max_spell_level() * CR["SPELLCASTING"]
            )

        # SAVING_THROWS
        cr_settings["SAVING_THROWS"] = (
            len(self._saving_throws_list) * CR["SAVING_THROWS"]
        )

        # Senses
        for sense, value in self._senses_dict.items():
            cr_settings["SENSES"] += ((value / 30) * CR["SENSES"][sense])

        # DAMAGE_RESISTANCES
        for damage_type in self._damage_resistances_list:
            cr_settings["DAMAGE_RESISTANCES"] += CR["DAMAGE_RESISTANCES"][damage_type]

        # DAMAGE_VULNERABILITIES
        for damage_type in self._damage_vulnerabilities_list:
            cr_settings["DAMAGE_VULNERABILITIES"] += CR["DAMAGE_VULNERABILITIES"][damage_type]

        # DAMAGE_IMMUNITIES
        for damage_type in self._damage_immunities_list:
            cr_settings["DAMAGE_IMMUNITIES"] += CR["DAMAGE_IMMUNITIES"][damage_type]

        # CONDITION_IMMUNITIES
        for condition_type in self._condition_immunities_list:
            cr_settings["CONDITION_IMMUNITIES"] += CR["CONDITION_IMMUNITIES"][condition_type]

        # Create CR Average
        cr_average = math.floor(
            statistics.mean(cr_base.values()) + sum(cr_settings.values())
        )

        # Return
        challenge_rating = get_cr_from_row(int(cr_average))
        return challenge_rating, cr_settings, cr_base

    def get_cr_defense(self):
        """
        Gets our Defensive Challenge Rating
        """

        return cr_defense(self.get_hp_average(), self._armors.get_ac())

    def get_cr_offense(self):
        """
        Gets our Offensive Challenge Rating
        """

        # Vars to calculate and be considered
        damage_per_round = 0
        to_hit = 0
        spell_dc = 8

        # Since weapon is first, we just make it our max DPR and to_hit
        damage_per_round = (
            self._weapons.get_dpr_max() *
            self._attacks_per_round
        )
        to_hit = self._weapons.get_to_hit_max()

        # Leveled Cantrips, if applicable.
        if self.is_spell_caster():

            # Set our Spell DC
            spell_dc = max(self._spells.get_save_dc(), spell_dc)

            # Top?
            damage_per_round = max(
                self._spells.get_max_dpr(self._expected_cr),
                damage_per_round
            )
            to_hit = max(self._spells.get_to_hit(), to_hit)

        # Innate Cantrips, if applicable
        if self.is_innate_caster():

            # Sets our Spell DC
            spell_dc = max(self.innate.get_save_dc(), spell_dc)

            # Top?
            damage_per_round = max(
                self.innate.get_max_dpr(self._expected_cr),
                damage_per_round
            )
            to_hit = max(self.innate.get_to_hit(), to_hit)

        # Return
        return cr_offense(damage_per_round, to_hit, spell_dc)

    def get_extra(self, extra, dict_to_search):
        """
        Gets our Extra Value, given a Dict and Extra
        """

        if self.has_extra(extra, dict_to_search):
            return dict_to_search[extra]
        else:
            return 0

    def get_extra_trait(self, extra):
        """
        Gets our Extra Value, from Traits
        """

        return self.get_extra(extra, TRAITS)

    def get_formated_string(self, title, value, newline=True, dashes=True):
        """
        Returns a formated string, blank if value is empty
        """

        # We have a value?
        if not value:
            return ""

        # We want new lines?
        new_line_string = ""
        if newline:
            new_line_string = "\n"

        # We want dashes?
        dashes_string = ""
        if dashes:
            dashes_string = DASHES

        # Build out our return string
        return_string = ""
        if title:
            return_string = f"{new_line_string}{title}"

        # Now, add and return
        return (
            f"{return_string}{new_line_string}"
            f"{value}{new_line_string}{dashes_string}"
        )

    def get_innate_string(self):
        """
        Gets our Innate SpellCasting as a String
        """

        # Can we cast innate spells?
        if not self.is_innate_caster() or not self.innate.has_spell():
            return ""

        # Innate DC
        innate_dc = self.innate.get_save_dc()

        # Innate ToHit
        innate_to_hit = number_signed(self.innate.get_to_hit())

        # Good!  Let us build that there statement.
        innate_string = (
            f"INNATE SPELLCASTING.\nThe {self._name}'s innate "
            f"spellcasting ability is {self.innate.get_stat().name}"
            f" (spell save DC {innate_dc}, {innate_to_hit} to hit with spell"
            f" attacks). It can innately cast the following spells, requiring"
            f"no material components:\n"
        )

        # Cantrips?
        if len(self.innate.get_cantrips()):
            innate_string = (
                f"{innate_string}\nAt-will:"
                f"{spaced_list(self.innate.get_cantrips(), ', ')}"
            )

        # Casts Per Day (Leveled)
        for casts_per_day in range(1, self.innate.get_max_spell_level()):

            # Get Spells of this level.
            innate_spell_list = self.innate.get_spell_list(casts_per_day)

            # Spells?
            if len(innate_spell_list):
                innate_string = (
                    f"{innate_string}\n{casts_per_day}/day: "
                    f"{spaced_list(innate_spell_list , ', ')}"
                )

        # Return!
        return f"\n{innate_string}\n{DASHES}"

    def get_hp(self, value):
        """
        Get HP, validates our value
        """

        hp = value + self.get_hp_con_addition()
        if hp < 1:
            return 1
        return hp

    def get_hp_average(self):
        """
        Get HP Average
        """

        return self.get_hp(math.ceil(self._hit_dice.get_average()))

    def get_hp_con_addition(self):
        """
        Get HP Con Addition
        """

        return (
            self._stats.get_stat_bonus(StatsEnum.CONSTITUTION.value) *
            self._hit_dice._count
        )

    def get_hp_rolled(self):
        """
        Gets HP Rolled
        """

        return self.get_hp(math.ceil(self._hit_dice.roll_sum_single()))

    def get_list_names_string(self, title, list_of_enums):
        """
        Gets a List, using the name attribute (for enum)
        """

        # Return string
        return_string = ""

        # We have data?
        if len(list_of_enums):

            # List of names
            names = []

            # Create a list of the names.
            for enum in list_of_enums:
                names.append(enum.name)

            # Edit our Return String
            return_string = f"\n{title}. {spaced_list(names, ', ')}"

        # Return!
        return return_string

    def get_loot(self):
        """
        Gets Loot!
        """

        # Loot!? What is our CR?
        cr, _, _ = self.get_cr()

        # Roll a d100! (really a d99... we count 0 as 100)
        die = Dice(99, 1).roll_single()

        # Now, get our monies!
        list_of_dice_rolls = LOOT[cr][die]

        # Set it.
        total_money = []
        for i in list_of_dice_rolls:
            if i is not None:
                total_money.append(i.roll_sum_single())
            else:
                total_money.append(0)

        # Return the money!
        return (
            f"CP: {total_money[0]} SP: {total_money[1]} "
            f"EP: {total_money[2]} GP {total_money[3]} "
            f"PP {total_money[4]}"
        )

    def get_movement_string(self):
        """
        Gets our Movement Speeds
        """

        # Movement List
        movements = []

        # Iterate, creating the movement string.
        for movement, speed in self._movement_dict.items():

            # String
            movement_string = ""
            if movement is not MovementEnum.WALK:
                movement_string = f"{movement.name}: "

            # Append
            movements.append(f"{movement_string}{speed}ft")

        # Return it!
        return spaced_list(movements, ', ')

    def get_passive_skill(self, skill):
        """
        Gets our Passive Skill
        """

        return 10 + self.get_skill_bonus(skill)

    def get_prof_bonus(self):
        """
        Gets our Prof Bonus from our Expected CR
        """

        monster_stats = get_monster_stats_from_cr(self._expected_cr)
        return monster_stats[MonsterStatsByCrEnum.PROF_BONUS]

    def get_recharge_die_calculation(self):
        """
        We need to know our recharge die value?
        """

        if (
            self.get_extra_trait(ExtrasEnum.RECHARGE_TYPE) ==
            RechargeTypeEnum.GROUP_LEVEL
        ):
            if ClassEnum.RECHARGE in self._class_dict:
                return 7 - self._class_dict[ClassEnum.RECHARGE]
            return 1
        return 0

    def get_rvii_string(self):
        """
        Gets our DAMAGE_RESISTANCES, Vulnerabilities, Immunities
        and CONDITION_IMMUNITIES as a String
        """

        # Return!
        return "{}{}{}{}".format(
            self.get_list_names_string(
                "DAMAGE_RESISTANCES", self._damage_resistances_list
            ),
            self.get_list_names_string(
                "DAMAGE_VULNERABILITIES",
                self._damage_vulnerabilities_list
            ),
            self.get_list_names_string(
                "DAMAGE_IMMUNITIES",
                self._damage_immunities_list
            ),
            self.get_list_names_string(
                "CONDITION_IMMUNITIES",
                self._condition_immunities_list
            )
        )

    def get_saving_throws_string(self):
        """
        Gets SAVING_THROWS String
        """

        # SAVING_THROWS list to return
        saving_throws = []

        # Iterate our SAVING_THROWS
        for saving_throw in self._saving_throws_list:
            saving_throw_bonus = (
                self.get_prof_bonus() +
                self._stats.get_stat_bonus(saving_throw)
            )
            saving_throws.append(
                f"{saving_throw.name} {number_signed(saving_throw_bonus)}"
            )

        # Return String
        return self.get_formated_string(
            "\nSAVING_THROWS ", spaced_list(saving_throws, ', '),
            False, False
        )

    def get_senses_string(self):
        """
        Gets Senses String
        """

        # Senses list to return.
        senses = []

        # Iterate our Senses
        for sense, value in self._senses_dict.items():
            senses.append(f"{sense.name}: {value}")

        # Return
        return self.get_formated_string(
            "", spaced_list(senses, 'ft, ', True),
            False, False
        )

    def get_skill_bonus(self, skill):
        """
        Gets the Skill Bonus for an individual skill, including StatWeight
        """

        # We iterate the possible skills, looking for the skill
        # we have an existing bonus in.	 When we find it, we
        # return it with its bonus increased by the associated stat.
        for stat in SKILLS:	 # STRENGTH, DEXTERITY...

            # Skill here?
            if skill in SKILLS[stat]:

                # Grab the skill bonus we have for it
                skill_bonus = self._skill_bonus_dict[skill]

                # Depending on the main Stat for this skill, we then
                # add Stat Weight
                stat_weight = self._stats.get_stat_bonus(stat.value)

                # Return
                return (skill_bonus + stat_weight)

        # didn't find it.
        return 0

    def get_skills_string(self):
        """
        Get Skills we have a unique bonus in as a List
        """

        # Skills list to return.
        skills = []

        # Iterate our Skill Bonuses
        for skill, value in self._skill_bonus_dict.items():

            # Get the Skill Bonus Total, if we have a base bonus
            if value != 0:
                skills.append(
                    f"{skill.name} "
                    f"{number_signed(self.get_skill_bonus(skill))}"
                )

        # Return
        return self.get_formated_string(
            "\nSkills: ", spaced_list(skills, ', '),
            False, False
        )

    def get_special_function(self, special):
        """
        Gets a Special Ability's Function
        """

        return SPECIALS[special][SpecialsEnum.EXTRA][ExtrasEnum.FUNCTION]

    def get_special_result(self, special):
        """
        Gets a Special Ability Result
        """

        # Execute the String as Code
        exec(self.get_special_function(special)[1])

        # Now that it is stored in this instance, we call it.
        return locals()[self.get_special_function(special)[0]](self)

    def get_special_string(self, action, spacer="\n"):
        """
        Get Special Ability String
        """

        # Special Results
        specials = []

        # Iterate Special
        for name in SPECIALS:

            # Special Data
            data = SPECIALS[name]

            # What type?
            if action == data[SpecialsEnum.TYPE]:

                # Check Function
                if self.get_special_result(name):
                    specials.append(
                        f"{name}. "
                        f"{data[SpecialsEnum.DESCRIPTION].format(self)}"
                    )

        # Return
        return f"{spaced_list(specials, spacer)}"

    def get_special_and_traits_string(self, title, action,):
        """
        Gets a combination of our Specil and Traits
        """

        # Return String
        return_string = ""

        # Special String
        special_string = self.get_special_string(action)

        # Traits String
        traits_string = self.get_traits_string(action)

        # Add Traits
        return_string = f"{traits_string}"

        # Since we order it, Traits and then Special, if we have
        # Special AND Traits data, we need a new line
        if traits_string and special_string:
            return_string = f"{return_string}\n"

        # Add Special
        return_string = f"{return_string}{special_string}"

        # Return!
        return self.get_formated_string(title, return_string)

    def get_spell_save_dc_highest(self):
        """
        Gets our Highest Save DC of Innate and Spells
        """

        # Set vars
        innate_save_dc = spell_save_dc = 8 + self.get_prof_bonus()

        # Innate?
        if self.is_innate_caster():
            innate_save_dc = self.innate.get_save_dc()

        # Spells?
        if self.is_spell_caster():
            spell_save_dc = self._spells.get_save_dc()

        # Return
        return max(innate_save_dc, spell_save_dc)

    def get_spells_string(self):
        """
        Gets our Spell Data as a String
        """

        # No data?
        if not self.is_spell_caster() or not self._spells.has_spell():
            return ""

        # Return var.
        spell_string = ""

        # Caster Level, with th.. etc.
        caster_level = number_ord(
            self._class_dict[ClassEnum.SPELLCASTER][SpellCasterEnum.LEVEL]
        )

        # save DC8
        save_dc = self._spells.get_save_dc()

        # to hit
        to_hit = number_signed(self._spells.get_to_hit())

        # Build it!
        spell_string = (
            f"SPELLCASTING.\nThe {self._name} is a {caster_level}"
            f"-level spellcaster. Its spellcasting ability is"
            f"{self._spells.get_stat().name} (spell save DC {save_dc},"
            f"{to_hit} to hit with spell attacks.)  It has the"
            f"following spells prepared:\n"
        )

        # Cantrip
        if len(self._spells.get_cantrips()):
            spell_string = (
                f"{spell_string}\nCantrips (at will): "
                f"{spaced_list(self._spells.get_cantrips(), ', ')}"
            )

        # Leveled?
        for spell_level in range(1, self._spells.get_max_spell_level()):
            spells = self._spells.get_spell_list(spell_level)
            if spells:
                spell_string = (
                    f"{spell_string}\n{number_ord(spell_level)} "
                    f"Level ({self._spells._spells_per_level[spell_level]} "
                    f"slots): {spaced_list(spells, ', ')}"
                )

        # Return
        return f"\n{spell_string}\n{DASHES}"

    def get_traits_string(self, action_type, spacer="\n"):
        """
        Gets Traits, returning a string of each trait formatted with
        Squigglies removed.
        """

        # Traits to return
        traits = []

        # Trait Recharge Group
        trait_recharge_group = []

        # Iterate!
        for name in self._traits_list:

            # Trait Data
            data = TRAITS[name]

            # The type we want?
            if action_type == data[TraitsEnum.TYPE]:

                # Replaces Bracket Values with REAL values!
                description = data[TraitsEnum.DESCRIPTION].format(self)

                # String, formatted.
                trait_string = f"{name}. {description}"

                # This have recharge?
                if (
                    ExtrasEnum.RECHARGE_TYPE in data[TraitsEnum.EXTRA] and
                    data[TraitsEnum.EXTRA][ExtrasEnum.RECHARGE_TYPE] == RechargeTypeEnum.GROUP_LEVEL
                ):
                    trait_recharge_group.append(trait_string)
                else:
                    traits.append(trait_string)

        # Trait recharge group?
        if len(trait_recharge_group):

            # We have a recharge default?
            recharge_die = 6
            if ClassEnum.RECHARGE in self._class_dict:
                recharge_die = self._class_dict[ClassEnum.RECHARGE]

            # Recharge string
            recharge_string = "6"
            if recharge_die != 6:
                recharge_string = f"{recharge_die} - {recharge_string}"

            # Recharge Die
            if len(traits):
                traits.append("\n")
            traits.append(f"RECHARGE ACTIONS ({recharge_string})")
            traits.extend(trait_recharge_group)

        # Data?
        return self.get_formated_string(
            "", spaced_list(traits, spacer), False, False
        )

    def get_weapon_property_count(self, action_property, included=True):
        """
        Used for our Special Function
        """

        return self._weapons.get_property_count(action_property, included)

    def has_extra(self, extra, dict_to_search):
        """
        Do we have this extra?
        """

        return extra in dict_to_search

    def has_extra_from_list(
        self, extra, list_to_search,
        dict_to_search, extra_enum
    ):
        """
        Do we have this extra?
        """

        for item in list_to_search:
            if self.has_extra(extra, dict_to_search[item][extra_enum]):
                return True
        return False

    def has_extra_in_armor(self, extra):
        """
        Has extra specifically in Armor
        """

        return self._armors.has_extra(extra)

    def has_monster_property(self, monster_property):
        """
        We have the given monster property?
        """

        if monster_property in self._monster_properties_list:
            return True
        return False

    def is_extra_size_or_race(self, extras):
        """
        Given an extra, does it have race or size requirements?
        """

        # We meet the requirements?
        race_requirement_met = True
        size_requirement_met = True

        # Sizes
        if (
            ExtrasEnum.SIZES_REQUIRED in extras and
            self._size not in extras[ExtrasEnum.SIZES_REQUIRED]
        ):
            size_requirement_met = False
        elif (
            ExtrasEnum.SIZES_EXEMPT in extras and
            self._size in extras[ExtrasEnum.SIZES_EXEMPT]
        ):
            size_requirement_met = False

        # Races
        if (
            ExtrasEnum.RACES_REQUIRED in extras and
            self._race not in extras[ExtrasEnum.RACES_REQUIRED]
        ):
            race_requirement_met = False
        elif (
            ExtrasEnum.RACES_EXEMPT in extras and
            self._race in extras[ExtrasEnum.RACES_EXEMPT]
        ):
            race_requirement_met = False

        # Return!
        return size_requirement_met and race_requirement_met

    def is_spell_caster(self):
        """
        Are we a caster?
        """

        # Caster?
        if ClassEnum.SPELLCASTER in self._class_dict:
            return True

        # Nope!
        return False

    def is_innate_caster(self):
        """
        INNATECASTING?
        """

        # Any spells?
        if ClassEnum.INNATECASTER in self._class_dict:
            return True

        # Boooo
        return False

    def remove_armor(self, armor):
        """
        Removes an armor from our armor list
        """

        self._armors.remove(armor)

    def remove_saving_throw(self, saving_throw):
        """
        Removes a saving throw from our saving throw list
        """

        if saving_throw in self._saving_throws_list:
            self._saving_throws_list.remove(saving_throw)

    def remove_spell(self, spell, spell_level, instance):
        """
        Removes Spells
        """

        instance.remove(spell, spell_level)

    def remove_trait(self, trait):
        """
        Removes a trait
        """

        if trait in self._traits_list:
            self._traits_list.remove(trait)

    def remove_weapon(self, weapon):
        """
        Removes a weapon from our weapon list
        """

        self._weapons.remove(weapon)

    def setup_innate(self):
        """
        Sets up InnateCaster Spells
        """

        # Are we an InnateCaster?
        if not self.is_innate_caster():
            return None

        # InnateCaster List
        innate_caster_list = self._class_dict[ClassEnum.INNATECASTER]

        # Create Spells
        self.innate = Spells(
            self._stats,
            self.get_prof_bonus(),
            innate_caster_list[InnateCasterEnum.STAT],
            INNATE_SPELLS_PER_LEVEL,
            SPELLS
           )

        # Add Spells
        for spell in innate_caster_list[InnateCasterEnum.SPELL_DICT]:
            self.add_spell(
                spell, innate_caster_list[InnateCasterEnum.SPELL_DICT][spell],
                self.innate
            )

    def setup_spells(self):
        """
        Sets up SpellCaster Spells
        """

        # Are we a SpellCaster?
        if not self.is_spell_caster():
            return None

        # SpellCaster List
        spell_caster_list = self._class_dict[ClassEnum.SPELLCASTER]

        # Create Spells
        self._spells = Spells(
            self._stats,
            self.get_prof_bonus(),
            spell_caster_list[SpellCasterEnum.STAT],
            SPELLS_BY_LEVEL[spell_caster_list[SpellCasterEnum.LEVEL]],
            SPELLS
           )

        # Add Spells
        for spell in spell_caster_list[SpellCasterEnum.LIST]:
            self.add_spell(
                spell, SPELLS[spell][SpellsEnum.LEVEL],
                self._spells
            )

    def __str__(self):
        """
        Print-Out
        """

        # Calculate Challenge Rating
        challenge_rating, _, _ = self.get_cr()

        # Bonus Action
        bonus_action = self.get_special_and_traits_string(
            "Bonus Actions", ActionTypesEnum.BONUS
        )

        # Other
        other_actions = self.get_special_and_traits_string(
            "Other", ActionTypesEnum.NONE
        )

        # Reactions
        reactions = self.get_special_and_traits_string(
            "Reactions", ActionTypesEnum.REACTION
        )

        # Standard Actions
        standard_actions = self.get_special_and_traits_string(
            "", ActionTypesEnum.STANDARD
        )

        # Return it!
        return (
                f"\n{self._name:<30s}{self._alignment:<20s}"
                f"\n{self._size.name} {self._race.name}"
                f"\n{DASHES}"
                f"\nArmor Class {self._armors.get_ac()} ({self._armors})"
                f"\nHit Points {self._hp} ({self._hit_dice})"
                f"\nSpeed {self.get_movement_string()}"
                f"\n{DASHES}"
                f"{self._stats}"
                f"\n{DASHES}"
                f"{self.get_saving_throws_string()}{self.get_skills_string()}"
                f"{self.get_rvii_string()}"
                f"\nSenses: {self.get_senses_string()}passive perception"
                f"{self.get_passive_skill(SkillsEnum.PERCEPTION)}"
                f"\nLanguages: {spaced_list(self._languages_list, ', ')}"
                f"\nChallenge {challenge_rating}"
                f"({ get_xp_by_cr(challenge_rating)} xp)"
                f"\n{DASHES}"
                f"{self.get_innate_string()}"
                f"{self.get_spells_string()}"
                f"\nActions ({self._attacks_per_round})"
                f"\n{self._weapons.print()}"
                f"\n{DASHES}"
                f"{standard_actions}{bonus_action}{reactions}{other_actions}"
                f"\nLOOT\n{self.get_loot()}"
           )


class MonsterWrapper(Monster):
    """
    Wrapper for the Monster class, exposes a function within string.format
    """

    @property
    def get_spell_save_dc_highest(self):
        return super(MonsterWrapper, self).get_spell_save_dc_highest()
    @property
    def get_armor_disadvantage_on_stealth_string(self):
        return super(MonsterWrapper, self).get_armor_disadvantage_on_stealth_string()
