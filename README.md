# 5eMonsterVariants
5e Monster Variants, created by attempting to keep the CR the same with chnages.

# Instructions
git submodule update --init --remote --recursive

# TODO
- Maximum Stat of 30
- Weapons Line 57, dice has no update method
- Monster Variants access stats and hp.. modify monster get_hp and get_stats
- New Option for selection.  CR Adjustment Calculator.  If we are off on CR, tries to find
    what adjustment to the base calculation values would be required to get all our monsters
    aligned with their expected CR.
- Export JSON from Monster?  This is a static string/int version for graphics
- Fix Monster Variants
    = Need to Test Adding/Remove Weapons and Armor
    = With Natural Weapons.  Should we have something on the weapon that lists a RACE type?
        ~ IE Dragons can use Claw/Tail/Bite?
- More Loot!
- Legendary Actions
- Random Names for Monsters?
    = We'd prolly need a RaceEnum to then go out and fetch based off of from a fantasy generator
