# 5eMonsterVariants
5e Monster Variants, created by attempting to keep the CR the same with chnages.

# Instructions
git submodule update --init --remote --recursive

# TODO
- Monster Variants access stats and hp.. modify monster get_hp and get_stats
- uhm... python phyics for better rolling... :D?
- New Option for selection.  CR Adjustment Calculator.  If we are off on CR, tries to find
    what adjustment to the base calculation values would be required to get all our monsters
    aligned with their expected CR.
- Export JSON from Monster?  This is a static string/int version for graphics
- Fix Monster Variants
    = Need to Test Adding/Remove Weapons and Armor
    = With Natural Weapons.  Should we have something on the weapon that lists a RACE type?
        ~ IE Dragons can use Claw/Tail/Bite?	
- For Variants.  Disabilities?
    = Like... one legged?  .75% speed?  Could be a "trait"?  Or special.
- More Loot!
- Legendary Actions
- Expand Variant Monsters to build an encounter
    = ... not sure on this one...
- Random Names for Monsters?
    = We'd prolly need a RaceEnum to then go out and fetch based off of from a fantasy generator
- Dice Tool?
    = 3d DICE w/ physics
    = or same 2d dice, but with more random; hitting sides reduces "speed" by x and etc.
        ~ Maybe sudo physics?
- Encounter Tool?
    = If in JS React Import JSON from monster variants?
    = Use Dice tool for monster rolls
    = Have Monster stats appear as well as keep track of current hp
        ~ If we exporting to JSON.  Need to export more data than before?  Like almost as if each
        monster is its own package.
