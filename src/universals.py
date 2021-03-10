"""

    universals.py

    Universal classes/functions.

"""

# Sys
import ast
import json
import os

# Moinee
from .dice import Dice
from .enumerators import (
    ArmorSlotsEnum, ActionPropertiesEnum, ActionTypesEnum,
    ClassEnum, ConditionTypesEnum, DamageTypesEnum, ExtrasEnum,
    MonsterPropertiesEnum, MovementEnum, RaceEnum, RechargeTypeEnum,
    SenseEnum, SizeEnum, SkillsEnum, StatsEnum
)
from .modular.rangeddict import RangedDict
from .settings import JSON_DIR


# Dict of Public Enums, used in JSON Encode/Decode
JSON_ENUMS = {
    "ArmorSlotsEnum": ArmorSlotsEnum,
    "ActionPropertiesEnum": ActionPropertiesEnum,
    "ActionTypesEnum": ActionTypesEnum,
    "ClassEnum": ClassEnum,
    "ConditionTypesEnum": ConditionTypesEnum,
    "DamageTypesEnum": DamageTypesEnum,
    "ExtrasEnum": ExtrasEnum,
    "MonsterPropertiesEnum": MonsterPropertiesEnum,
    "MovementEnum": MovementEnum,
    "RaceEnum": RaceEnum,
    "RechargeTypeEnum": RechargeTypeEnum,
    "SenseEnum": SenseEnum,
    "SizeEnum": SizeEnum,
    "SkillsEnum": SkillsEnum,
    "StatsEnum": StatsEnum
}


def convert_keys(obj, convert=str):
    """
    Convert the given object into convert type
    """

    if isinstance(obj, list):
        return [convert_keys(i, convert) for i in obj]
    elif isinstance(obj, dict):
        return {convert(k): convert_keys(v, convert) for k, v in obj.items()}
    return convert(obj)


def get_actual_from_compound(compound, dictionary):
    """
    Given a split, gets our actual name and scale
    """

    # Split!
    data = compound.split("_")

    # Name
    name = data[0]

    # Valid?
    if name in dictionary:

        # No scale?
        scale = 0
        if len(data) > 1 and data[1]:
            scale = int(data[1])

        # Return!
        return name, scale

    # NOPE!
    else:
        raise KeyError()


def get_json_data(json_file):
    """
    Gets JSON Data
    """

    # Build the path
    json_file_path = f"{JSON_DIR}/{json_file}.json"

    # The path exists?
    if os.path.exists(json_file_path):

        # Open the JSON file
        json_file_read = open(json_file_path, "r")

        # Parse
        json_file_parsed = convert_keys(
            json.load(
                json_file_read
            ), json_decoder
        )

        # Return
        return json_file_parsed

    # Path did not exist!
    return {}


def json_encoder(key):
    """
    JSON Encoder
    """

    # If this is a registered Enum, append __enum__
    if type(key) in JSON_ENUMS.values():
        return f"__enum__{key}"

    # If this is a Dice roll, append __dice__ then the sides and count
    elif isinstance(key, Dice):
        return f"__dice__{key.sides},{key.count}"

    # If this is a RangeDict
    elif isinstance(key, RangedDict):

        # Return String
        return_string = convert_keys(key.to_json(), json_encoder)

        # Return it!117011
        return f"__rangedict__{return_string}"

    # Return the rest.
    return key


def json_decoder(value):
    """
    JSON Decoder
    """

    # Since Strings are appended class types, we only want them.
    if not isinstance(value, str):
        return value

    # RangeDict?
    # Needs to happen before ENUM/DICE
    elif "__rangedict__" in value:

        # List of values.
        # We use ast.literal_eval to take the list as a string
        # and properly make it is a list
        list_of_values = ast.literal_eval(value.split("__rangedict__")[1])

        # ReEEEEeturn!
        # We have to call convert_keys on the list incase there are enum
        # or dice in it.
        return range_dict_from_list(convert_keys(list_of_values, json_decoder))

    # Enum?
    elif "__enum__" in value:

        # We get the Enum by parsing out the first __enum__
        name, member = value.split("__enum__")[1].split(".")

        # Return the Enum
        return getattr(JSON_ENUMS[name], member)

    # Dice?
    elif "__dice__" in value:

        # Split
        dice_values = value.split("__dice__")[1].split(",")

        # Create and return.
        return Dice(int(dice_values[0]), int(dice_values[1]))

    # Regular ol' string
    else:
        return value


def number_signed(number):
    """
    Simply returns our plus or minus number
    """

    return "{0:+g}".format(number)


def number_ord(number):
    """
    Returns st, nd, or th
    https://stackoverflow.com/questions/3644417/python-format-datetime-with-st-nd-rd-th-english-ordinal-suffix-like
    """
    return str(number) + (
        "th" if 4 <= (number % 100) <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(
            (number % 10), "th"
        )
    )


def print_debug_dict(dict_to_print, key_length=0, value_length=0):
    """
    Given a dictionary to print, will print it.
    Optional Positional adjustment
    Sizes off of largest key/value, up to 40.
    """

    # Gets our Largest Key
    if not key_length:
        key_length = min(max(len(k) for k in dict_to_print.keys()), 40)

    # Not Value Length?
    if not value_length:
        value_length = key_length

    # Print eit!
    print(
        '\n'.join(
            [
                f"{str(key):>{key_length}} {str(value):<{key_length}}"
                for key, value in dict_to_print.items()
            ]
        )
    )


def range_dict_from_list(list_to_convert):
    """
    Wrapper for the RangeDict class.  Takes in a list and makes a RangeDict.
    Format is [[min, max, value], ...]
    """

    # New RangeDict
    rd = RangedDict()

    # Iterate the list, creating our RangeDict
    for sublist in list_to_convert:

        # Add and go on.
        rd[(sublist[0], sublist[1])] = sublist[2]

    # Return eit!
    return rd


def spaced_list(list, spacer='\n', include_at_end=False):
    """
    Given a list and a spacer '\n', ', '... etc, returns that list formated.
    """
    return spacer.join(map(str, list)) + ("", spacer)[include_at_end]


# We gotta be included!
if __name__ == '__main__':
    pass
