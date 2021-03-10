"""

    spells.py

    Spells module

"""

# mmmiiiNNEee
from .enumerators import ExtrasEnum, SpellsEnum


__all__ = [ "Spells" ]


class Spells( ):
    """
    Spellzzz
    """


    def __init__( self, stats, prof_bonus, spell_stat, spells_per_level, data ):
        """
        Constructor!
        """

        # Set Class vars        
        self._data = data
        self._prof_bonus = prof_bonus
        self._spell_stat = spell_stat
        self._spells_per_level = spells_per_level
        self._stats = stats             

        # Create our spell dictionary
        self._spell_dict = {} 
        for spell_level in range( len( spells_per_level ) ):
            if spells_per_level[ spell_level ]:
                self._spell_dict[ spell_level ] = []
            else:
                break


    def add( self, spell, spell_level ):
        """
        Add the given spell to our dict
        The reason we ask for a spell level, even though we can look it up
        is because for Innate we use the spell level to determine
        how many times per day we can cast a spell
        """

        # Don't already have this spell?
        if self.has_spell( spell ):
            return False

        # Valid Spell level to add to?
        if spell_level in self._spell_dict:
            self._spell_dict[ spell_level ].append( spell )
            self._spell_dict[ spell_level ].sort()
        else:
            return False


    def get_cantrips( self ):
        """
        Gets our cantrips
        """

        return self.get_spell_list( 0 )


    def get_max_dpr( self, cr ):
        """
        Gets our max dpr cantrip
        """

		# Current top DPR
        damage_per_round = 0
		
		# Iterate
        for cantrip in self.get_cantrips():
		
			# Cantrip Damage Dice
            damage_dice = self.get_extra( cantrip, ExtrasEnum.DAMAGE_DICE )

            # We have Damage Dice?
            if damage_dice is not None:

				# Is this DPR higher than what we already have?  If so, store it and store its to_hit.
                damage_per_round = max( damage_dice.get_average(), damage_per_round )

        # Return
        return damage_per_round


    def get_extra( self, spell, extra ):
        """
        If we have the given extra, returns it.  Otherwise, returns None
        """

        if extra in self._data[ spell ][ SpellsEnum.EXTRA ]:
            return self._data[ spell ][ SpellsEnum.EXTRA ][ extra ]
        else:
            return None

    
    def get_max_spell_level( self ):
        """
        Gets our max spell level
        """

        return max( self._spell_dict, key = int )


    def get_save_dc( self ):
        """
        Gets our Save DC
        """

        return 8 + self.get_to_hit()

    
    def get_spell_list( self, spell_level ):
        """
        Gets a list of spells, given a spell level
        """
        
        if spell_level in self._spell_dict:
            return self._spell_dict[ spell_level ]
        else:
            return []


    def get_spells_single_list( self, start_level = 0 ):
        """
        Returns a large list of all our spells, starting at a level.
        """

        # All the spells!
        all_the_spells = []

        # Iterate
        for spell_level in range( start_level, len( self._spell_dict ) ):
            for spell in self.get_spell_list( spell_level ):
                all_the_spells.append( spell )

        # Return em!
        return all_the_spells


    def get_stat( self ):
        """
        Gets the Spells Stat
        """

        return self._spell_stat


    def get_stat_bonus( self ):
        """
        Gets our Spell stat Bonus
        """

        return self._stats.get_stat_bonus( self.get_stat() )

    
    def get_to_hit( self ):
        """
        Gets our To Hit
        """

        return self._prof_bonus + self.get_stat_bonus()


    def has_spell( self, spell = None ):
        """
        Empty spell = do we have any spell at all?
        """
	
		# Iterate Spell Level List, seeing if we have this spell.
        for spell_level in self._spell_dict:
		
			# Get List of Spells
            spell_list = self._spell_dict[ spell_level ]
			
			# Check it!
            if ( not spell and len( spell_list ) > 0 ) or spell in spell_list:
                return True
		
		# Nope
        return False            


    def remove( self, spell, spell_level ):
        """
        Remove the given spell from our dict
        """

        # We have this spell?
        if not self.has_spell( spell ):
            return False
        
        # Remove
        if spell_level in self._spell_dict:
            self._spell_dict[ spell_level ].remove( spell )


# We gotta be included!
if __name__ == '__main__':
    pass