"""

    monster_variants.py

    https://dmdave.com/how-to-create-a-dd-monster-for-fifth-edition-in-15-minutes-or-less/

    Notes
    . If a Trait has a DC in it, an Innate or Spells Class needs to be added.

"""

# Sys
from collections import Counter
import statistics

# Moinnee
from src.challengerating import get_cr_row
from src.monster import MonsterWrapper
from src.monstervariant import MonsterVariant
from src.universals import get_json_data, print_debug_dict

# ARMOR
ARMOR = get_json_data("armor")

# Individual Monster Stats
monsters_json = get_json_data("monsters")
MONSTERS = {}
for m in monsters_json.keys():
    MONSTERS[m] = MonsterWrapper(m, *monsters_json[m])

# SPELLS
SPELLS = get_json_data("spells")

# TRAITS
TRAITS = get_json_data("traits")

# WEAPONS
WEAPONS = get_json_data("weapons")


def get_count_input(text, minimum=0, maximum=1000):
    """
    Get count input
    """

    while True:
        count = input(f"{text} ")
        if count.isdigit():
            count = int(count)
            if count in range(minimum, maximum):
                return int(count)


def get_cumulative_information(monster):
    """
    Get Cumulative Information
    """

    # Total to return
    cr_total = Counter({})

    # Grab our Data
    cr, cr_settings, cr_base = MONSTERS[monster].get_cr()

    # Increment!
    cr_total += Counter(cr_settings) + Counter(cr_base)

    # Return!
    return cr, cr_total


def get_monster_input():
    """
    Get a monster!
    """

    while True:
        monster = input("Which Monster? ")
        if monster in MONSTERS:
            return monster


def option_create_variant():
    """
    Create variant
    """

    # Get our Monster Data
    monster = MONSTERS[get_monster_input()]

    # How many we want?
    count = get_count_input("How Many?")

    # Count can't be less than one.
    if count < 1:
        count = 1

    # Iterate!
    for _ in range(count):

        # Create the Variant
        variant_monster = MonsterVariant(
            monster, WEAPONS, ARMOR, TRAITS, SPELLS
            )
        variant_monster.create()
        print(variant_monster)
        print(variant_monster._iterations)


def option_get_cr_accumulation():
    """
    Gets CR Accumulation, which is the total in each CR Score that
    exists between all Monsters
    """

    # Data to doodle
    cr_total = Counter({})

    # Iterate
    for name in MONSTERS.keys():
        _, cr_combined = get_cumulative_information(name)
        cr_total += cr_combined

    # Print Debug
    print_debug_dict(cr_total)


def option_get_cr_calculation():
    """
    Get a Single Monster's CR Calculations
    """

    # Get our Monster Data
    monster = get_monster_input()

    # Get Data
    _, cr_combined = get_cumulative_information(monster)

    # Get and Print!
    print_debug_dict(cr_combined)


def option_get_cr_difference():
    """
    Get CR Difference
    """

    # Iterate and load the data
    for key, value in MONSTERS.items():

        cr, cr_combined = get_cumulative_information(key)

        # Is this a different CR than expected?
        if cr != value.expected_cr:
            print(f"\n{key} Expected ({value.expected_cr}) Received ({cr})")
            print_debug_dict(cr_combined)


def option_get_cr_tweaks():
    """
    Attempts to Tweak our CR settings to fix issues.
    """

    # Settings test
    # settings.CR["RECHARGE"] = .01

    # Different CR Lists

    # Iterate our monsters
    for name, value in MONSTERS.items():

        # Geeeeit!
        cr, cr_settings, cr_base = value.get_cr()

        od_average = statistics.mean(cr_base.values())

        settings_sum = sum(cr_settings.values())

        print(name, get_cr_row(value.expected_cr), od_average, settings_sum)

        """

        for key in settings.CR.keys():

            v = cr_settings[key]
            if v != 0:
                print(key, cr_settings[key])

        # Not correct?
        #if cr != value.expected_cr:

            # Which is our max key?
            #max_key = max(cr_settings, key = cr_settings.get)

            #print(max_key)
            #print_debug_dict(cr_settings)

        """


def option_print_all_monsters():
    """
    Print all the monsters!
    """

    for monster in MONSTERS:
        print(MONSTERS[monster])


def option_print_single_monster():
    """
    Print a Single Monster
    """

    print(MONSTERS[get_monster_input()])


class Option():
    """
    An option!
    """

    def __init__(self, name, function):
        self.name = name
        self.function = function


# Options
options = [
    Option("Create Variant", option_create_variant),
    Option("Get CR Accumulation", option_get_cr_accumulation),
    Option("Get CR Calculation", option_get_cr_calculation),
    Option("Get CR Differences", option_get_cr_difference),
    Option("Get CR Tweaks", option_get_cr_tweaks),
    Option("Print Single Monster", option_print_single_monster),
    Option("Print All Monsters", option_print_all_monsters)
]

# Turn our options list into purty print.
print('\n'.join(f"{o}. {options[o].name:<20}" for o in range(0, len(options))))

# Choice
options[get_count_input("?", 0, len(options))].function()
