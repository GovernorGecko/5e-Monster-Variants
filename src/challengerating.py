"""

    challengerating.py

    Challenge Rating or CR, is used to determine how tough a NPC in DnD 5e is.
    This module provides the tables used by DnD 5e as well as
    functions for calculating
    the challenge rating of a NPC, given certain stats.

"""

# Moin
from .enumerators import MonsterStatsByCrEnum


# Monster Statistics By Challenge Rating
# CR, Prof Bonus, AC, Hit Points Min, Hit Points Max, Attack Bonus, Damage
# a Round Min, Damage a Round Max, Save DC
MONSTER_STATS_BY_CR = [
    [0, 		2,	13, 1,	    6, 	    3, 	0, 	1, 	13],
    [0.125, 	2, 	13, 7, 	    25,     3, 	2, 	3, 	13],
    [0.25, 	2,	13, 26, 49,     3, 	    4, 	5, 	13],
    [0.5, 		2,	13, 50,     70,     3, 	6, 	8, 	13],
    [1, 		2, 	13, 71,     85,     3, 	9, 	14, 13],
    [2, 		2, 	13, 86,     100,    3, 	15, 20, 13],
    [3, 		2, 	13, 101,    115,    4, 	21, 26, 13],
    [4, 		2, 	14, 116,    130,    5, 	27, 32, 14],
    [5, 		3, 	15, 131,    145,    6, 	33, 38, 15],
    [6, 		3, 	15, 146,    160,    6, 	39, 44, 15],
    [7, 		3, 	15, 161,    175,    6, 	45, 50, 15],
    [8, 		3, 	16, 176,    190,    7, 	51, 56, 16],
    [9, 		4, 	16, 191,    205,    7, 	57, 62, 16],
    [10, 		4, 	17, 206,    220,    7, 	63, 68, 16],
    [11, 		4, 	17, 221,    235,    8, 	69, 74, 17],
    [12, 		4, 	17, 236,    250,    8, 	75, 80, 17],
    [13, 		5, 	18, 251,    265,    8, 	81, 86, 18],
    [14, 		5, 	18, 266,    280,    8, 	87, 92, 18],
    [15, 		5, 	18, 281,    295,    8, 	93, 98, 18],
    [16, 		5, 	18, 296,    310,    9,	99,     104,    18],
    [17, 		6, 	19, 311,    325,    10,	105,    110,    19],
    [18, 		6, 	19, 326,    340,    10, 111,    116,    19],
    [19, 		6, 	19, 341,    355,    10, 117,    122,    19],
    [20, 		6, 	19, 356,    400,    10, 123,    140,    19],
    [21, 		7, 	19, 401,    445,    11, 141,    158,    20],
    [22, 		7, 	19, 446,    490,    11, 159,    176,    20],
    [23, 		7, 	19, 491,    535,    11, 177,    194,    20],
    [24, 		7, 	19, 536,    580,    12, 195,    212,    21],
    [25, 		8, 	19, 581,    625,    12, 213,    230,    21],
    [26, 		8, 	19, 626,    670,    12, 231,    248,    21],
    [27, 		8, 	19, 671,    715,    13, 249,    266,    22],
    [28, 		8, 	19, 716,    760,    13, 267,    284,    22],
    [29, 		9, 	19, 761,    805,    13, 285,    302,    22],
    [30, 		9, 	19,	808,    850,    14, 303,    320,    23]
]

# Monster XP By CR
MONSTER_XP_BY_CR = {
    0		:	10,
    0.125	:	25,
    0.25	:	50,
    0.5		:	100,
    1		:	200,
    2		:	450,
    3		:	700,
    4		:	1100,
    5		:	1800,
    6		:	2300,
    7		:	2900,
    8		:	3900,
    9		:	5000,
    10		:	5900,
    11		:	7200,
    12		:	8400,
    13		:	10000,
    14		:	11500,
    15		:	13000,
    16		:	15000,
    17		:	18000,
    18		:	20000,
    19		:	22000,
    20		:	25000,
    21		:	33000,
    22		:	41000,
    23		:	50000,
    24		:	62000,
    25		:	75000,
    26		:	90000,
    27		:	105000,
    28		:	120000,
    29		:	135000,
    30		:	155000
}

# Encounter Difficulty XP per Character
# Level of PC, Easy, Medium, Hard, Deadly
ENCOUNTER_DIFFICULTY_XP_PER_CHARACTER = {
    1	:	[	25,		50,		75,		100		],
    2	:	[	50,		100,	150,	200		],
    3	:	[	75,		150,	225,	400		],
    4	:	[	125,	250,	375,	500		],
    5	:	[	250,	500,	750,	1100	],
    6	:	[	300,	600,	900,	1400	],
    7	:	[	350,	750,	1100,	1700	],
    8	:	[	450,	900,	1400,	2100	],
    9	:	[	550,	1100,	1600,	2400	],
    10	:	[	600,	1200,	1900,	2800	],
    11	:	[	800,	1600,	2400,	3600	],
    12	:	[	1000,	2000,	3000,	4500	],
    13	:	[	1100,	2200,	3400,	5100	],
    14	:	[	1250,	2500,	3800,	5700	],
    15	:	[	1400,	2800,	4300,	6400	],
    16	:	[	1600,	3200,	4800,	7200	],
    17	:	[	2000,	3900,	5900,	8800	],
    18	:	[	2100,	4200,	6300,	9500	],
    19	:	[	2400,	4900,	7300,	10900	],
    20	:	[	2800,	5700,	8500,	12700	]
}


def cr_defense(hp, ac):
    """
    Calculates our defense CR, given HP and AC
    Returns the Row our CR is on.
    """

    return cr_calculation(
        hp, MonsterStatsByCrEnum.MIN_HP,
        MonsterStatsByCrEnum.MAX_HP, ac, MonsterStatsByCrEnum.AC
        )


def cr_offense(damage_per_round, attack_bonus, save_dc):
    """
    Calculates our offense CR, given damage per round, attack bonus and save dc
    Returns the Row our CR is on.
    """

    # This is slightly different than Defense CR.  We take the greater cr
    # of attack bonus vs save dc and return it
    attack_bonus_cr = cr_calculation(
        damage_per_round, MonsterStatsByCrEnum.DAMAGE_PER_ROUND_MIN,
        MonsterStatsByCrEnum.DAMAGE_PER_ROUND_MAX, attack_bonus,
        MonsterStatsByCrEnum.ATTACK_BONUS
        )
    save_dc_cr = cr_calculation(
        damage_per_round, MonsterStatsByCrEnum.DAMAGE_PER_ROUND_MIN,
        MonsterStatsByCrEnum.DAMAGE_PER_ROUND_MAX, save_dc,
        MonsterStatsByCrEnum.SAVE_DC
        )

    # Return the highest.
    return max(attack_bonus_cr, save_dc_cr)


def cr_calculation(
    comparison_value, comparison_maximum_index,
    comparison_minimum_index, comparison_difference_value,
    comparison_difference_index
):
    """
    Calculates CR.  Used for Offense or Defense.
    """

    # CR Row
    cr_row = 0

    # Iterate, seeing which CR Row we are on.
    for i in range(0, len(MONSTER_STATS_BY_CR)):

        compare_max = MONSTER_STATS_BY_CR[i][comparison_maximum_index]
        compare_min = MONSTER_STATS_BY_CR[i][comparison_minimum_index]

        # We in this range?
        if comparison_value >= compare_max and comparison_value <= compare_min:

            # Store the row.
            cr_row = i

            # Difference
            comparison = MONSTER_STATS_BY_CR[i][comparison_difference_index]
            difference = comparison_difference_value - comparison

            # CR Difference
            cr_row = cr_row + int(difference / 2)

            # We done
            break

    # Make sure our cr_row is valid
    if cr_row < 0:
        cr_row = 0

    # Return
    return cr_row


def get_cr_from_row(row):
    """
    Gets our CR given a Row number.
    """

    return MONSTER_STATS_BY_CR[row][MonsterStatsByCrEnum.CR]


def get_cr_row(cr):
    """
    Gets our CR Row, given a CR number.
    """

    for i in range(0, len(MONSTER_STATS_BY_CR)):
        if MONSTER_STATS_BY_CR[i][MonsterStatsByCrEnum.CR] == cr:
            return i


def get_monster_stats_from_cr(cr):
    """
    Gets our Monster Stats, given a CR
    """

    return MONSTER_STATS_BY_CR[get_cr_row(cr)]


def get_xp_by_cr(cr):
    """
    Gets our XP, given a CR
    """

    return MONSTER_XP_BY_CR[cr]


# We gotta be included!
if __name__ == '__main__':
    pass
