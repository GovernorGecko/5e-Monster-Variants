"""

    monstervariant.py

    CR Is Determined by two things; DEF(HP, AC) and OFF(DPR, PROF, SPELLDC)
    So to tweak these, we'll need to adjust stats until we match up.

"""

# Sys
from copy import deepcopy
import random

# Meeeaaaine
from .enumerators import MonsterPropertiesEnum


__all__ = ["MonsterVariant"]


class MonsterVariant():
    """
    A Monster Variant
    """

    # Constss
    MINIMUM_ITERATIONS = 10

    def __init__(self, monster, weapons, armor, traits, spells):
        """
        Constructor!
        """

        # Store Lists
        self._armor = armor
        self._spells = spells
        self._traits = traits
        self._weapons = weapons

        # Set CR to -1 and iterations
        self._iterations = 0
        self._variant_cr = -1

        # Set base and copy variant
        self._base_monster = monster
        self._variant_monster = deepcopy(monster)

        # Get Base Monster CR
        self._base_monster_cr = self._base_monster.get_cr()

        # Get our lowest stat
        self._lowest_base_stat = self._base_monster._stats.get_stat(
            self._base_monster._stats.get_lowest_stat()
        )

    def __str__(self):
        """
        To string!
        """

        return str(self._variant_monster)

    def create(self):
        """
        Create a Variant!
        """

        # Reset Iteration
        self._iterations = 0

        # Let's GOOooo
        while self._variant_cr != self._base_monster_cr:

            # Revert them stats, time to reassign!
            self._variant_monster._stats.revert_stats(self._lowest_base_stat)

            # Balance em!
            self._variant_monster._stats.create_balanced_stats()

            # Set our new HP
            self._variant_monster._hp = self._variant_monster.get_hp_rolled()

            # WEAPONS
            if not self._variant_monster.has_monster_property(
                MonsterPropertiesEnum.NO_VARIANT_WEAPON
            ):

                # Removing?
                if random.random() > 0.5 and len(
                    self._variant_monster._weapons._weapon_list
                ) > 1:

                    # Remove a Random Weapon!
                    self._variant_monster.remove_weapon(
                        random.choice(
                            self._variant_monster._weapons._weapon_list
                        )
                    )

                # Adding!
                elif len(self._variant_monster._weapons._weapon_list) < 3:

                    # Get a Random Weapon!
                    random_weapon = random.choice(list(self._weapons))

                    # Creates the Random Weapon
                    self._variant_monster.add_weapon(random_weapon)

            # ARMOR
            if not self._variant_monster.has_monster_property(
                MonsterPropertiesEnum.NO_VARIANT_ARMOR
            ):

                # Removing?
                # Unlike Weapon, we are okay with the
                # creature not having Armor.
                if random.random() > 0.5:

                    # Remove a Random Armor!
                    if len(self._variant_monster._armors._armor_list):
                        self._variant_monster.remove_armor(
                            random.choice(
                                self._variant_monster._armors._armor_list
                            )
                        )

                # Adding!
                else:

                    # Get a Random Armor!
                    random_armor = random.choice(list(self._armor))

                    # Creates the Random Armor
                    self._variant_monster.add_armor(random_armor)

            # TRAITS

            # INNATE

            # SPELLS

            # We want a minimum number of iterations, so we
            # don't begin updating until after those happen.
            if self._iterations > self.MINIMUM_ITERATIONS:
                self._variant_cr = self._variant_monster.get_cr()

            # Iterate!
            self._iterations += 1


# We gotta be included!
if __name__ == '__main__':
    pass
