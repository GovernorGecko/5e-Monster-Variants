"""

	_json_editor
	
"""

# Sys
import json

# Minee
from dice import Dice
from enumerators import ArmorSlotsEnum, ActionPropertiesEnum, ActionTypesEnum, ClassEnum, ConditionTypesEnum, DamageTypesEnum, ExtrasEnum, MonsterPropertiesEnum, MovementEnum, RaceEnum, RechargeTypeEnum, SenseEnum, SizeEnum, SkillsEnum, StatsEnum
from universals import convert_keys, get_json_data, json_encoder, range_dict_from_list
import settings

# ARMOR
# For Natural armor, we name it NATUARL-ACBONUS
# NAME_#(bonus ac) : [ AC BASE BONUS, SLOT, [ MONSTER PROPERTIES ], { EXTRAS } ]
ARMOR = {
	"NATURAL" : [ 0, ArmorSlotsEnum.CHEST, [ MonsterPropertiesEnum.NATURAL_ARMOR ], {} ],
	"LEATHER" : [ 1, ArmorSlotsEnum.CHEST, [ MonsterPropertiesEnum.SIMPLE ], {} ], 
	"STUDDED" : [ 2, ArmorSlotsEnum.CHEST, [ MonsterPropertiesEnum.MARTIAL ], {} ],
	"BREASTPLATE" : [ 4, ArmorSlotsEnum.CHEST, [ MonsterPropertiesEnum.MARTIAL ], { ExtrasEnum.DEXTERITY_CAP: 2 }],
	"SCALE" : [ 4, ArmorSlotsEnum.CHEST, [ MonsterPropertiesEnum.MARTIAL ], { ExtrasEnum.DEXTERITY_CAP: 0, ExtrasEnum.STEALTH_DISADVANTAGE: True } ],
	"CHAINMAIL" : [ 6, ArmorSlotsEnum.CHEST, [ MonsterPropertiesEnum.SIMPLE ], { ExtrasEnum.DEXTERITY_CAP: 0, ExtrasEnum.STRENGTH_REQUIREMENT: 13, ExtrasEnum.STEALTH_DISADVANTAGE: True } ], 
	"SHIELD" : [ 2, ArmorSlotsEnum.SHIELD, [ MonsterPropertiesEnum.TWOHANDED ], {} ]
}

# MONSTERS
# Name : [ Size, Race, Alignment, # Hit Dice, Expected CR, Attacks Per Round, Movements, Class, Stats [STR, CON, DEX, INT, WIS, CHA], Saving Throws, Skill Bonuses, Senses, Languages, Traits, Weapons, Armor, MonsterProperties, DVuls, DRes, DImm, CImm ]
MONSTERS = {	
	"DEATH DOG" : [SizeEnum.MEDIUM, RaceEnum.MONSTROSITY, "NEUTRAL EVIL", 6, 1, 2, { MovementEnum.WALK: 40 }, {}, [15, 14, 14, 3, 13, 6], [], {SkillsEnum.PERCEPTION: 4, SkillsEnum.STEALTH: 2}, {SenseEnum.DARKVISION: 120}, [], ["INFECTIOUS", "TWOHEADED"], ["BITE_0"], [], [MonsterPropertiesEnum.TWOHEADED, MonsterPropertiesEnum.NATURAL_WEAPON, MonsterPropertiesEnum.NO_VARIANT_ARMOR, MonsterPropertiesEnum.NO_VARIANT_WEAPON], [], [], [], []],
	"DUST MEPHIT" : [SizeEnum.SMALL, RaceEnum.ELEMENTAL, "NEUTRAL EVIL", 5, 0.5, 1, {MovementEnum.WALK: 30, MovementEnum.FLY: 30}, { ClassEnum.INNATECASTER: [ StatsEnum.CHARISMA, { "SLEEP": 1 } ] }, [ 5, 14, 10, 9, 11, 10 ], [], {SkillsEnum.PERCEPTION: 2, SkillsEnum.STEALTH: 2}, {SenseEnum.DARKVISION: 60}, ["AURAN", "TERRAN"], ["DEATH BURST", "BLINDING BREATH"], ["CLAW_0"], [], [MonsterPropertiesEnum.BREATH, MonsterPropertiesEnum.BURST, MonsterPropertiesEnum.NATURAL_WEAPON, MonsterPropertiesEnum.NO_VARIANT_WEAPON, MonsterPropertiesEnum.NO_VARIANT_ARMOR, MonsterPropertiesEnum.SIMPLE], [], [DamageTypesEnum.FIRE], [DamageTypesEnum.POISON], [ConditionTypesEnum.POISONED]],
	"GOBLIN" : [SizeEnum.SMALL, RaceEnum.GOBLINOID, "NEUTRAL EVIL", 2, 0.25, 1, { MovementEnum.WALK: 30 }, {}, [ 8, 14, 10, 10, 8, 8 ], [], {SkillsEnum.STEALTH: 4}, { SenseEnum.DARKVISION: 60 }, ["COMMON", "GOBLIN"], ["NIMBLE ESCAPE"], ["SCIMITAR_0", "SHORTBOW_0"], ["LEATHER", "SHIELD"], [ MonsterPropertiesEnum.SIMPLE, MonsterPropertiesEnum.TWOHANDED ], [], [], [], [] ],
	"NOBLE" : [ SizeEnum.MEDIUM, RaceEnum.HUMANOID, "ANY ALIGNMENT", 2, 0.125, 1, {MovementEnum.WALK : 30}, {}, [ 11, 11, 12, 12, 14, 16 ], [], {SkillsEnum.DECEPTION: 2, SkillsEnum.INSIGHT: 2, SkillsEnum.PERSUASION: 2}, {SenseEnum.DARKVISION: 5}, ["ANY LANGUAGES"], ["PARRY"], ["RAPIER_0"], ["BREASTPLATE"], [MonsterPropertiesEnum.BREATH, MonsterPropertiesEnum.SIMPLE, MonsterPropertiesEnum.MARTIAL, MonsterPropertiesEnum.TWOHANDED], [], [], [], [] ],
	"SILVER DRAGON WYRMLING" : [SizeEnum.MEDIUM, RaceEnum.DRAGON, "LAWFUL GOOD", 6, 2, 1, {MovementEnum.WALK: 30, MovementEnum.FLY: 60}, { ClassEnum.INNATECASTER: [ StatsEnum.CHARISMA, {}]}, [19, 10, 17, 12, 11, 15], [], {SkillsEnum.PERCEPTION: 4, SkillsEnum.STEALTH: 2}, {SenseEnum.BLINDSIGHT: 10,SenseEnum.DARKVISION: 60},["DRACONIC"],["COLD BREATH", "PARALYZING BREATH"], ["BITE_4"], ["NATURAL_7"], [MonsterPropertiesEnum.NATURAL_WEAPON, MonsterPropertiesEnum.NATURAL_ARMOR, MonsterPropertiesEnum.NO_VARIANT_WEAPON, MonsterPropertiesEnum.NO_VARIANT_ARMOR, MonsterPropertiesEnum.BREATH], [], [], [DamageTypesEnum.COLD], [] ]
}


# SPECIAL
# Dual Wield, requires us to have more than one Melee weapon
# and one LIGHT weapon
function_dual_wield = """def function_dual_wield( self ): return ( self.get_weapon_property_count( ActionPropertiesEnum.RANGE, False ) >= 2 and self.get_weapon_property_count( ActionPropertiesEnum.LIGHT ) > 0 )"""
# Armor Sneak Penalty.
# Some armor adds a Sneak Penalty.  This is in Extra Enums
function_disadvantage_on_stealth = """def function_disadvantage_on_stealth( self ): return self.has_extra_in_armor( ExtrasEnum.STEALTH_DISADVANTAGE )"""

# These aren't to be added by Variant.  They are checked for CR and display purposes.
# NAME : [ ACTION, DESCRIPT, [ MONSTER PROPERTIES ], { EXTRAS } ]
SPECIAL = {
	"DISADVANTAGE ON STEALTH": [ ActionTypesEnum.NONE, "Wearing {0.get_armor_disadvantage_on_stealth_string} incurs a Disadvantage to Sneak skill rolls.", [ ], { ExtrasEnum.CR_MODIFIER: -1, ExtrasEnum.FUNCTION: ["function_disadvantage_on_stealth", function_disadvantage_on_stealth ] } ],
	"DUAL-WIELD": [ ActionTypesEnum.BONUS, "{0._name} can wield a LIGHT weapon in their offhand, attacking with it but not adding the Stat Bonus to damage.", [ MonsterPropertiesEnum.TWOHANDED ], { ExtrasEnum.CR_MODIFIER: 1, ExtrasEnum.FUNCTION: [ "function_dual_wield", function_dual_wield ] } ]
}

# SPELLS
# Spells really only play a big role in Variant if they are a Cantrip (level 0)
# In this case, we need a Damage Die if applicable to determine DPR for CR Offense
# NAME: [ LEVEL, [ MONSTER PROPERTIES ], { EXTRAS } ]
SPELLS = {
	"FIREBOLT": [ 0, [ MonsterPropertiesEnum.SIMPLE ], { ExtrasEnum.DAMAGE_DICE: range_dict_from_list( [ [ 0, 4, Dice( 10, 1 ) ], [ 5, 10, Dice( 10, 2 ) ], [ 11, 16, Dice( 10, 3 ) ], [ 17, 99, Dice( 10, 4 ) ] ] ) } ],
	"LIGHT" : [ 0, [ MonsterPropertiesEnum.SIMPLE ], {} ],
	"SLEEP": [ 1, [ MonsterPropertiesEnum.SIMPLE ], {} ],
	"CHARM": [ 1, [ MonsterPropertiesEnum.SIMPLE ], {} ]
}

# TRAITS
# Traits are... extra abilities.. That aren't spells/weapons.
# NAME : [ ACTION, DESCRIPT, [ MONSTER PROPERTIES ], { EXTRAS } ]
TRAITS = {
	"BLINDING BREATH" : [ ActionTypesEnum.STANDARD, "The {0._name} exhales a 15- foot cone of blinding dust. Each creature in that area must succeed on a DC {0.get_spell_save_dc_highest} Dexterity saving throw or be blinded for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.", [ MonsterPropertiesEnum.BREATH ], { ExtrasEnum.RECHARGE_TYPE: RechargeTypeEnum.GROUP_LEVEL } ], 
	"COLD BREATH" : [ ActionTypesEnum.STANDARD, "The {0._name} exhales an icy blast in a 15-foot cone. Each creature in that area must make a DC {0.get_spell_save_dc_highest} Constitution saving throw, taking 18 (4d8) cold damage on a failed save, or half as much damage on a successful one.", [ MonsterPropertiesEnum.BREATH ], {ExtrasEnum.RECHARGE_TYPE: RechargeTypeEnum.GROUP_LEVEL} ],
	"PARALYZING BREATH" : [ ActionTypesEnum.STANDARD, "The {0._name} exhales paralyzing gas in a 15-foot cone. Each creature in that area must succeed on a DC {0.get_spell_save_dc_highest} Constitution saving throw or be paralyzed for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.", [ MonsterPropertiesEnum.BREATH ], {ExtrasEnum.RECHARGE_TYPE: RechargeTypeEnum.GROUP_LEVEL} ],
	"DEATH BURST" : [ ActionTypesEnum.REACTION, "When the {0._name} dies, it explodes in a burst of dust. Each creature within 5 feet of it must then succeed on a DC {0.get_spell_save_dc_highest} Constitution saving throw or be blinded for 1 minute. A blinded creature can repeat the saving throw on each of its turns, ending the effect on itself on a success.", [ MonsterPropertiesEnum.BURST], { } ],
	"INFECTIOUS" : [ ActionTypesEnum.NONE, "Whenever {0._name} hits with a melee natural attack, if the target is a creature, it must succeed on a DC 12 Constitution saving throw against disease or become poisoned until the disease is cured. Every 24 hours that elapse, the creature must repeat the saving throw, reducing its hit point maximum by 5 (1d10) on a failure. This reduction lasts until the disease is cured. The creature dies if the disease reduces its hit point maximum to 0.", [ MonsterPropertiesEnum.NATURAL_WEAPON ], { ExtrasEnum.CR_MODIFIER: 1 } ],
	"NIMBLE ESCAPE" : [ ActionTypesEnum.BONUS, "{0._name} can take the Disengage or Hide Action", [], { ExtrasEnum.CR_MODIFIER: 1, ExtrasEnum.SIZES_REQUIRED : [ SizeEnum.SMALL ] } ],
	"PARRY" : [ ActionTypesEnum.REACTION, "{0._name} adds 2 to its AC against one melee attack that would hit it. To do so, the {0._name} must see the attacker and be wielding a melee weapon.", [ MonsterPropertiesEnum.MARTIAL ], { ExtrasEnum.CR_MODIFIER: 1 } ],
	"TWOHEADED" : [ ActionTypesEnum.NONE, "{0._name} has advantage on Wisdom (Perception) checks and on saving throws against being blinded, charmed, deafened, frightened, stunned, or knocked unconscious.", [ MonsterPropertiesEnum.TWOHEADED ], { ExtrasEnum.CR_MODIFIER: 1 } ]
}

# WEAPONS
# NAME : [ DAMAGE_TYPE, DAMAGE_DICE, [ PROPERTIES ], [ MONSTER PROPERTIES ], { EXTRAS } ]
WEAPONS = {
	"BITE" : [ DamageTypesEnum.PIERCING, Dice( 6, 1 ), [], [ MonsterPropertiesEnum.NATURAL_WEAPON ], {} ],
	"CLAW"	: [ DamageTypesEnum.SLASHING,  Dice( 4, 1 ), [ ActionPropertiesEnum.FINESSE ], [ MonsterPropertiesEnum.NATURAL_WEAPON ], {} ],	
	"DAGGER" : [ DamageTypesEnum.PIERCING, Dice( 4, 1 ), [ ActionPropertiesEnum.THROWN, ActionPropertiesEnum.LIGHT, ActionPropertiesEnum.FINESSE ], [ MonsterPropertiesEnum.SIMPLE ], { ExtrasEnum.RANGE: "20/60" } ],
	"LONGSWORD" : [ DamageTypesEnum.SLASHING, Dice( 8, 1 ), [], [ MonsterPropertiesEnum.MARTIAL], { ExtrasEnum.VERSATILE: "LONGSWORD_2" } ],
	"RAPIER" : [ DamageTypesEnum.PIERCING, Dice( 8, 1 ), [ ActionPropertiesEnum.FINESSE ], [ MonsterPropertiesEnum.MARTIAL ], {} ],
	"SCIMITAR" : [ DamageTypesEnum.SLASHING, Dice( 6, 1 ), [ ActionPropertiesEnum.LIGHT, ActionPropertiesEnum.FINESSE ], [ MonsterPropertiesEnum.SIMPLE ], {} ],
	"SHORTBOW" : [ DamageTypesEnum.PIERCING, Dice( 6, 1 ), [ ActionPropertiesEnum.AMMUNITION, ActionPropertiesEnum.RANGE ], [ MonsterPropertiesEnum.TWOHANDED, MonsterPropertiesEnum.SIMPLE ], { ExtrasEnum.RANGE: "80/320", ExtrasEnum.IMPROVISED: "IMPROVISED_0"  } ],
	"IMPROVISED" : [ DamageTypesEnum.NONE, Dice( 4, 1 ), [ ActionPropertiesEnum.NO_ADD ], [], {} ]
}

# Dictionaries
dicts = {
	"ARMOR" 	: ARMOR,
	"MONSTERS"	: MONSTERS,
	"SPECIAL"	: SPECIAL,
	"SPELLS"	: SPELLS,
	"TRAITS"	: TRAITS,
	"WEAPONS" 	: WEAPONS
}

# Which do we want?
dict_to_encode = input( "Which dictionary: " )

# Valid dictionary?
if dict_to_encode in dicts.keys():

	# Encode the json
	dict_encoded = json.dumps( convert_keys( dicts[ dict_to_encode ], json_encoder ) )

	# Write it to the file.
	with open( f"{settings.JSON_DIR}/{str( dict_to_encode ).lower()}.json", 'w' ) as outfile:
		outfile.write( dict_encoded )

	# Print it!
	print( dict_encoded )

	# Decode!
	print( get_json_data( str( dict_to_encode ).lower() ) )