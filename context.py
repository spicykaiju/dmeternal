
# Conversation Tags

HELLO,SHOP,WEAPON,INFO,HINT = range(5)


class ContextTag( tuple ):
    def matches( self, other ):
        # A context tag matches self if each level defined in self matches
        # the equivalent level in other. Note that this is not reciprocal-
        # If of different lengths, the short can match the long but the long
        # won't match the short.
        return self[0:len(self)] == other[0:len(self)]


PRESENT = True
ABSENT = False
MAYBE = 999

# *****************************
# ***   RANDOM  MAP  TAGS   ***
# *****************************

ENTRANCE, GOAL = range( 2 )

# **************************************
# ***   Monster  Description  Tags   ***
# **************************************
#
# When selecting a monster, the candidate must match the scene habitat or EVERY,
# and should match at least one more tag in the scene description. If a monster
# of a given kind is requested it should match that too.
#
# Habitat Tags
HAB_EVERY, HAB_FOREST, HAB_CAVE = range( 3 )

# Description Tags
DES_EARTH, DES_AIR, DES_WATER, DES_FIRE, DES_SOLAR, DES_LUNAR = range(100,106)

# Type Tags
MTY_BEAST, MTY_HUMANOID, MTY_FIGHTER, MTY_THIEF, MTY_PRIEST, MTY_MAGE = range(200,206)

# Genus Tags. Note that these don't necessarily correspond to templates- a
#  necromancer monster may be grouped with the undead, despite not being undead
#  itself. Also a monster can have more than one genus because around here we
#  believe in multiple inheritence.
GEN_GIANT, GEN_GOBLIN, GEN_CHAOS, GEN_UNDEAD, GEN_NATURE = range( 300,305 )

def matches_description( context_set, desc_request ):
    # context_set is a list of context tags.
    # desc_request is a dictionary describing which tags are wanted.
    # Return a positive number if the two are in agreement, or 0 otherwise.
    num_matches = 0

    for k,v in desc_request.iteritems():
        if isinstance( k, tuple ):
            # We have multiple things to match.
            if v is PRESENT:
                if any( i in context_set for i in k ):
                    num_matches += 1
                else:
                    num_matches = 0
                    break
            elif v is ABSENT:
                if any( i not in context_set for i in k ):
                    num_matches += 1
                else:
                    num_matches = 0
                    break
        elif v is PRESENT:
            if k in context_set:
                num_matches += 1
            else:
                num_matches = 0
                break
        elif v is ABSENT:
            if k not in context_set:
                num_matches += 1
            else:
                num_matches = 0
                break
        elif v is MAYBE:
            if k in context_set:
                num_matches += 1

    return num_matches

