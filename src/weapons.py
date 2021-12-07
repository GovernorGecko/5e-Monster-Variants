"""

    weapons.py

    That which stores our weapons.  SUPER COMPLEX

"""

# Moine
from .enumerators import (
    ActionPropertiesEnum, ExtrasEnum, MonsterPropertiesEnum,
    SizeEnum, StatsEnum, WeaponsEnum
)
from .universals import get_actual_from_compound, number_signed, spaced_list


__all__ = ["SIZE_DAMAGE_DIE_COUNT", "Weapon", "Weapons"]


# SIZE - DAMAGE DIE COUNT
SIZE_DAMAGE_DIE_COUNT = {
    SizeEnum.LARGE 		: 1,
    SizeEnum.HUGE		: 2,
    SizeEnum.GARGANTUAN	: 3
}


class Weapon():
    """
    Stores base weapon information, as well as scales
    """

    __slots__ = [
        "_name", "_scale", "_stats", "_data",
        "_dice", "_improvised", "_versatile"
    ]

    def __init__(self, name, scale, stats, data, size_count_bonus):
        """
        Given a compound name and the weapon dict, creates a weapon.
        """

        # Store
        self._name = name
        self._scale = scale
        self._data = data[name]
        self._stats = stats

        # Optional Variables
        self._improvised = None
        self._versatile = None

        # Create the Dice
        self._dice = self._data[
            WeaponsEnum.DAMAGE_DICE
        ].get_scaled(self._scale)
        # self._dice.update(count=self._dice._count + size_count_bonus)

    def __str__(self):
        """
        Returns a string
        """

        return f"{self._name} {self._dice} {self._versatile}"

    def get_extra(self, extra):
        """
        Gets the given Extra, if we have it.
        """

        # We have it?
        if self.has_extra(extra):
            return self._data[WeaponsEnum.EXTRA][extra]
        else:
            return None

    def get_monster_properties(self):
        """
        Gets our monster properties
        """

        return self._data[WeaponsEnum.MONSTER_PROPERTIES]

    def get_name(self):
        """
        Gets our name.
        """

        return self._name

    def get_stat_bonus(self):
        """
        Gets our Stat Bonus
        """

        # STR/DEX Bonuses
        str_stat_bonus = self._stats.get_stat_bonus(StatsEnum.STRENGTH.value)
        dex_stat_bonus = self._stats.get_stat_bonus(StatsEnum.DEXTERITY.value)

        # If this is a Finesse weapon, use the higher of STR/DE
        if self.has_action_property(ActionPropertiesEnum.FINESSE):
            return max(str_stat_bonus, dex_stat_bonus)

        # Is this a RANGE weapon?
        elif self.has_action_property(ActionPropertiesEnum.RANGE):
            return dex_stat_bonus

        # Otherwise, use Strengt
        else:
            return str_stat_bonus

    def has_extra(self, extra):
        """
        We have the given extra?
        """

        return extra in self._data[WeaponsEnum.EXTRA]

    def has_action_property(self, action_property):
        """
        We have the given action property?
        """

        return action_property in self._data[WeaponsEnum.ACTION_PROPERTIES]

    # We have the given monster property?
    def has_monster_property(self, monster_property):
        return monster_property in self._data[WeaponsEnum.MONSTER_PROPERTIES]


class Weapons():
    """
    Weapons we got!
    """

    def __init__(self, stats, prof_bonus, size, data):
        """
        Constructor!
        """

        # Store
        self._data = data
        self._prof_bonus = prof_bonus
        self._stats = stats

        # Size Count Bonus
        self._size_count_bonus = 0
        if size in SIZE_DAMAGE_DIE_COUNT:
            self._size_count_bonus = SIZE_DAMAGE_DIE_COUNT[size]

        # Create our list
        self._weapon_list = []

    def __str__(self):
        """
        Spaced List Print
        """

        return self._weapon_list

    def add(self, weapon):
        """
        Add Weapon
        """

        self._weapon_list.append(weapon)

    def count(self, name=""):
        """
        How many weapons we have?
        """

        # No name?  We want it all.
        if not name:
            return len(self._weapon_list)

        # Name?  Get a count and return.
        else:
            count = 0
            for weapon in self._weapon_list:
                if weapon._name == name:
                    count += 1
            return count

    def create(self, compound, add=False):
        """
        The idea here, is this creates a Weapon, but doesn't store it.
        unless you set add to True
        """

        # Split the compound.
        name, scale = get_actual_from_compound(compound, self._data)

        # Create the weapon.
        weapon = Weapon(
            name, scale, self._stats,
            self._data, self._size_count_bonus
        )

        # Do we have Improvised Dice?
        if weapon.has_extra(ExtrasEnum.IMPROVISED):
            i_name, i_scale = get_actual_from_compound(
                weapon.get_extra(
                    ExtrasEnum.IMPROVISED
                ), self._data)
            weapon._improvised = Weapon(
                i_name, i_scale, self._stats,
                self._data, self._size_count_bonus
            )

        # Do we have Versatile Dice?
        if weapon.has_extra(ExtrasEnum.VERSATILE):
            v_name, v_scale = get_actual_from_compound(
                weapon.get_extra(
                    ExtrasEnum.VERSATILE
                ), self._data)
            weapon._versatile = Weapon(
                v_name, v_scale, self._stats,
                self._data, self._size_count_bonus
            )

        # Add?
        if add:
            self.add(weapon)
        else:
            return weapon

    def get_dpr_max(self):
        """
        Gets our max DPR with a weapon
        """

        # DPR
        damage_per_round = 0

        # Iterate our Weapons
        for weapon in self._weapon_list:

            # Damage Per Round
            damage_per_round = max(
                weapon._dice.get_average() + weapon.get_stat_bonus(),
                damage_per_round)

        # Return
        return damage_per_round

    def get_property_count(self, action_property, included=True):
        """
        Gets the number of properties in our weapons
        """

        # Return value
        count = 0

        # Iterate
        for weapon in self._weapon_list:

            # We find it?
            action_property_found = action_property in weapon._data[
                WeaponsEnum.ACTION_PROPERTIES
            ]

            # This what we want?
            if action_property_found is included:
                count += 1

        # Return!
        return count

    def get_to_hit_max(self):
        """
        Get To Hit Max
        """

        # To Hit
        to_hit = 0

        # Iterate our Weapons
        for weapon in self._weapon_list:

            # To Hit
            to_hit = max(weapon.get_stat_bonus(), to_hit)

        # Return
        return to_hit + self._prof_bonus

    def get_range(self, weapon):
        """
        If this weapon has a range, returns it.
        """

        return weapon.get_extra(ExtrasEnum.RANGE)

    def remove(self, weapon):
        """
        Removes the given weapon from our list
        """

        self._weapon_list.remove(weapon)

    def print(self):
        """
        Prints our weapon
        """

        # A list of the weapon data
        weapons = []

        # It.. er.. ATEEEEE
        for weapon in self._weapon_list:

            # To Hit
            to_hit_string = number_signed(
                self._prof_bonus + weapon.get_stat_bonus()
            )

            # Get Damage
            stat_bonus_signed = number_signed(weapon.get_stat_bonus())
            hit_damage = f"{weapon._dice}{stat_bonus_signed}"

            # Damage Type
            damage_type = weapon._data[WeaponsEnum.DAMAGE_TYPE].name

            # Weapon Attack Typ
            weapon_attack_type = "Melee"

            # Reach Base
            reach = "REACH 5FT"

            # Properties
            # Reach
            if weapon.has_action_property(ActionPropertiesEnum.REACH):
                reach = "REACH 10 FT"

            # Range
            if weapon.has_action_property(ActionPropertiesEnum.RANGE):
                reach = f"RANGE: {self.get_range(weapon)}FT"
                weapon_attack_type = "Ranged"

            # Thrown
            if weapon.has_action_property(ActionPropertiesEnum.THROWN):
                reach = f"{reach} (THROWN  {self.get_range(weapon)}FT)"

            # Versatile
            if weapon.has_extra(ExtrasEnum.VERSATILE):
                hit_damage = (
                    f"{hit_damage} ({weapon._versatile._dice}"
                    f"{number_signed(weapon.get_stat_bonus())})"
                )

            # Improvised
            if weapon.has_extra(ExtrasEnum.IMPROVISED):
                hit_damage = (
                    f"{hit_damage} ({weapon._improvised._dice}"
                    f"{stat_bonus_signed} IMPROVISED MELEE)"
                )

            # Extra Data: Light?
            extras_light = " "
            if weapon.has_action_property(ActionPropertiesEnum.LIGHT):
                extras_light = " (LIGHT) "

            # Weapon or Natural?
            weapon_composition_type = "Weapon"
            if weapon.has_monster_property(
                MonsterPropertiesEnum.NATURAL_WEAPON
            ):
                weapon_composition_type = "Natural"

            # Build the data.
            w_data = (
                f"{weapon._name}. {weapon_attack_type}"
                f" {weapon_composition_type} Attack: {to_hit_string}"
                f" TO HIT, {reach}., HIT: {hit_damage}{extras_light}"
                f"{damage_type} DAMAGE"
            )

            # Add it!
            weapons.append(w_data)

        # Return
        return spaced_list(weapons, "\n")


# We gotta be included!
if __name__ == '__main__':
    pass
