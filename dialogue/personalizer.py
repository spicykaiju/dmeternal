import voice

""" Style Guide: When writing dialogue, try to follow the following rules.
    - Do not use contractions.

    DRACONIAN: Reptiles hiss. And they never want something they can desire.

    DWARVEN: Dwarves use a lot of kennings in their speech. Think "The Mighty
    Thor".

    ELVEN: Lacks words with negative meanings, like "evil" or "ugly". Instead
    use the negation of a positive word- "ungood", "unlovely".

    ORCISH: This language is more efficient than regular English because it gets
    rid of trivialities like verb conjugation, a bunch of pronouns, and the "th"
    sound.

    STUPID: Uses slang that your English teacher would disapprove of and
    otherwise mangles the language.

    SMART: Why use a four letter word when there's a twelve letter alternative?

"""

class PTEntry( object ):
    def __init__( self, subtext, requires = {} ):
        self.subtext = subtext
        self.requires = requires
    def fits_voice( self, npc_voice ):
        ok = True
        for k,v in self.requires.iteritems():
            if v:
                # This key is required.
                ok = ok and ( k in npc_voice )
            else:
                # This key is prohibited.
                ok = ok and ( k not in npc_voice )
        return ok

PT_DATABASE = {
    "am looking for": (
        PTEntry( "seek", { voice.DRACONIAN: True } ),
        ),
    "anything":   (
        PTEntry( "stuff", { voice.STUPID: True } ),
        ),
    "buy":   (
        PTEntry( "purchase", { voice.SMART: True } ),
        ),
    "buy something":   (
        PTEntry( "get a thing", { voice.STUPID: True } ),
        PTEntry( "make a purchase", { voice.ELVEN: True } ),
        PTEntry( "lay down some coin", { voice.DWARVEN: True } ),
        ),
    'different':   (
        PTEntry( "divergent", { voice.SMART: True } ),
        PTEntry( "not the same", { voice.STUPID: True } ),
        PTEntry( "dissimilar", { voice.ELVEN: True } ),
        ),
    "Do you have":   (
        PTEntry( "You got", { voice.ORCISH: True } ),
        ),
    'exactly':   (
        PTEntry( "precisely", { voice.SMART: True } ),
        PTEntry( "perfectly", { voice.ELVEN: True } ),
        PTEntry( "right", { voice.STUPID: True } ),
        ),
    "have":   (
        PTEntry( "'ave", { voice.ORCISH: True } ),
        PTEntry( "haves", { voice.DRACONIAN: True, voice.STUPID: True } ),
        ),
    "have .":   (
        PTEntry( "possess.", { voice.DRACONIAN: True } ),
        ),
    "Hello":   (
        PTEntry( "'Ello, ello", { voice.ORCISH: True } ),
        PTEntry( "'Ello", { voice.ORCISH: True, voice.STUPID: False } ),
        PTEntry( "Greetings", { voice.SMART: True } ),
        PTEntry( "Hey", { voice.STUPID: True } ),
        PTEntry( "Salutations", { voice.DRACONIAN: True } ),
        PTEntry( "Hi", { voice.SMART: False, voice.DWARVEN: False, voice.ORCISH: False } ),
        PTEntry( "Lali-ho", { voice.DWARVEN: True } ),
        ),
    "Hello ,":   (
        PTEntry( "'Ello there,", { voice.ORCISH: True } ),
        PTEntry( "Greetingss,", { voice.DRACONIAN: True } ),
        PTEntry( "Lali-ho,", { voice.DWARVEN: True } ),
        ),
    "here":   (
        PTEntry( "'ere", { voice.ORCISH: True } ),
        ),
    "I am": (
        PTEntry( "I'm" ),
        ),
    "I would": (
        PTEntry( "I'd" ),
        ),
    "information": (
        PTEntry( "stuff", { voice.STUPID: True } ),
        PTEntry( "knowledge", { voice.SMART: True } ),
        PTEntry( "enlightenment", { voice.ELVEN: True, voice.STUPID: False } ),
        PTEntry( "know-wotz", { voice.ORCISH: True } ),
        PTEntry( "secrets", { voice.DRACONIAN: True } ),
        PTEntry( "truth", { voice.DWARVEN: True } ),
       ),
    "is not": (
        PTEntry( "isn't" ),
        PTEntry( "ain't", { voice.STUPID: True } ),
        ),
    "It is": (
        PTEntry( "It's" ),
        ),
    "Let me": (
        PTEntry( "Lemme", { voice.STUPID: True } ),
        PTEntry( "Allow me to", { voice.SMART: True } ),
        ),
    "Looking for": (
        PTEntry( "Lookin' for", { voice.ORCISH: True } ),
        PTEntry( "Seeking", { voice.DRACONIAN: True } ),
        ),
    "my":   (
        PTEntry( "me", { voice.ORCISH: True } ),
        PTEntry( "me", { voice.STUPID: True } ),
        ),
    "need":   (
        PTEntry( "needs", { voice.DRACONIAN: True } ),
        PTEntry( "require", { voice.STUPID: False } ),
        ),
    "sea": (
        PTEntry( "whale-road", { voice.DWARVEN: True } ),
       ),
    "see your wares": (
        PTEntry( "see what you have" ),
        PTEntry( "examine your wares", { voice.DWARVEN: True } ),
        PTEntry( "see your treasures", { voice.DRACONIAN: True } ),
        PTEntry( "look at yer gubbins", { voice.ORCISH: True } ),
        PTEntry( "peruse your wares", { voice.ELVEN: True } ),
        PTEntry( "inspect your merchandise", { voice.SMART: True } ),
        PTEntry( "look at your stuff", { voice.STUPID: True } ),
        ),
    "shop": (
        PTEntry( "store" ),
        PTEntry( "forge-front", { voice.DWARVEN: True } ),
        PTEntry( "boutique", { voice.ELVEN: True } ),
       ),
    "something": (
        PTEntry( "wotever", { voice.ORCISH: True } ),
       ),
    "sun": (
        PTEntry( "sky-candle", { voice.DWARVEN: True } ),
       ),
    "That": (
        PTEntry( "Dat", { voice.ORCISH: True } ),
       ),
    "that": (
        PTEntry( "dat", { voice.ORCISH: True } ),
       ),
    "that makes": (
        PTEntry( "wot makes", { voice.ORCISH: True } ),
       ),
    "The": (
        PTEntry( "Dat", { voice.ORCISH: True } ),
       ),
    "the": (
        PTEntry( "dat", { voice.ORCISH: True } ),
       ),
    "There is": (
        PTEntry( "There's" ),
        PTEntry( "Dere's", { voice.ORCISH: True } ),
       ),
    "There is not": (
        PTEntry( "There isn't", { voice.STUPID: False } ),
        PTEntry( "There ain't", { voice.STUPID: True } ),
        PTEntry( "Dere ain't", { voice.ORCISH: True } ),
        PTEntry( "Dere ain't no", { voice.ORCISH: True, voice.STUPID: True } ),
       ),
    "These": (
        PTEntry( "Deze", { voice.ORCISH: True } ),
       ),
    "these": (
        PTEntry( "deze", { voice.ORCISH: True } ),
       ),
    "This": (
        PTEntry( "Dis", { voice.ORCISH: True } ),
        PTEntry( "Thiss", { voice.DRACONIAN: True } ),
       ),
    "This is": (
        PTEntry( "Dis ere's", { voice.ORCISH: True } ),
        PTEntry( "This here's", { voice.ORCISH: True, voice.SMART: True } )
       ),
    "want": (
        PTEntry( "desire", { voice.DRACONIAN: True } ),
        ),
    "weapon": (
        PTEntry( "foe-smiter", { voice.DWARVEN: True } ),
        PTEntry( "head-cracker", { voice.ORCISH: True } ),
        PTEntry( "skull-smacker", { voice.ORCISH: True } ),
        PTEntry( "gutripper", { voice.ORCISH: True } ),
        PTEntry( "armament", { voice.SMART: True } ),
        PTEntry( "hurty thing", { voice.STUPID: True } ),
       ),
    "Welcome": (
        PTEntry( "Lali-ho", { voice.DWARVEN: True } ),
       ),
    "Welcome to": (
        PTEntry( "Git over ere to", { voice.ORCISH: True } ),
       ),
    "what": (
        PTEntry( "wot", { voice.ORCISH: True } ),
        ),
    "would like": (
        PTEntry( "desire", { voice.DRACONIAN: True } ),
        ),
    }

