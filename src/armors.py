"""

    armors.py

"""

# myhn
from .enumerators import ArmorEnum, ExtrasEnum, StatsEnum
from .universals import get_actual_from_compound, spaced_list


__all__ = ["Armor", "Armors"]


class Armor():
    """
    Armor!
    """

    def __init__(self, name, ac_bonus, data):
        """
        Constructor!
        """

        # Set Vars
        self._data = data
        self._name = name

        # Set our ac
        self._ac = ac_bonus + self._data[ArmorEnum.AC_BONUS]

    def has_extra(self, extra):
        """
        Has Extra
        """

        return extra in self._data[ArmorEnum.EXTRA]

    def get_extra(self, extra):
        """
        Get Extra
        """

        if self.has_extra(extra):
            return self._data[ArmorEnum.EXTRA][extra]
        else:
            raise KeyError

    def get_monster_properties(self):
        """
        Gets our monster properties!
        """

        return self._data[ArmorEnum.MONSTER_PROPERTIES]

    def get_name(self):
        """
        Gets our name
        """

        return self._name


class Armors():
    """
    All the Armors!
    """

    def __init__(self, stats, data):
        """
        Constructor!
        """

        # Vars
        self._data = data
        self._stats = stats

        # List of Armor
        self._armor_list = []

    def __str__(self):
        """
        Return String
        """

        armors = []
        for armor in self._armor_list:
            armors.append(armor._name)
        return spaced_list(armors, ", ")

    def add(self, armor):
        """
        Add Armor
        """

        self._armor_list.append(armor)

    def create(self, compound, add=False):
        """
        Create Armor
        """

        # Get name/value
        name, value = get_actual_from_compound(compound, self._data)

        # Create the Armor
        armor = Armor(name, value, self._data[name])

        # Return?
        if add:
            self.add(armor)
        else:
            return armor

    def get_ac(self):
        """
        Get AC
        """

        # AC Defaults to 10 when unarmored
        ac = 10

        # Dex Bonus
        dex_bonus = self._stats.get_stat_bonus(StatsEnum.DEXTERITY)

        # Do we have any armor?
        for armor in self._armor_list:

            # Add the ac
            ac = ac + armor._ac

            # Does it modify our dex?
            if armor.has_extra(ExtrasEnum.DEXTERITY_CAP):
                dex_bonus = min(
                    dex_bonus,
                    armor.get_extra(ExtrasEnum.DEXTERITY_CAP)
                   )

        # Return!
        return ac + dex_bonus

    def get_extra(self, extra):
        """
        Get Armor that has the given Extra
        """

        for armor in self._armor_list:
            if armor.has_extra(extra):
                return armor
        return None

    def has_armor(self, armor_to_check):
        """
        Has Armor
        """

        for armor in self._armor_list:
            if armor._name == armor_to_check._name:
                return True
        return False

    def has_extra(self, extra):
        """
        Any of our armor have this Extra?
        """

        for armor in self._armor_list:
            if armor.has_extra(extra):
                return True

    def has_slot(self, slot):
        """
        Has Armor Slot?
        """

        for armor in self._armor_list:
            if slot == armor._data[ArmorEnum.SLOT]:
                return True
        return False

    def has_slot_by_armor(self, armor):
        """
        Has Armor Slot, given armor!
        """

        return self.has_slot(armor._data[ArmorEnum.SLOT])

    def remove(self, armor):
        """
        Remove Armor?
        """

        if self.has_armor(armor):
            self._armor_list.remove(armor)


# We gotta be included!
if __name__ == '__main__':
    pass
