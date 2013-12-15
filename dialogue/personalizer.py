import voice

""" Style Guide: When writing dialogue, try to follow the following rules.
    - Do not use contractions.

    DRACONIAN: Reptiles hiss. And they never want something they can desire.

    DWARVEN: Dwarves use a lot of kennings in their speech. Think "The Mighty
    Thor".

    ELVEN: Lacks words with negative meanings, like "evil" or "ugly". Instead
    use the negation of a positive word- "ungood", "unlovely".

    GNOMIC: Like dwarves, but cheeky.

    GREEK: This pretty much only exists so that Centaurs, Titans, and other
    beings from Greek mythology can use the Green name generator. Maybe try to
    use as many loanwords as possible?

    KITTEH: I can haz lolspeak? Should have a big smart/stupid difference- the
    smart speakers get grammar right, just use Kitteh vocabulary. Also, try and
    stick to lolspeak which can be spoken aloud + isn't perfectly homophonic.

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
    "a lot":   (
        PTEntry( "lotz", { voice.KITTEH: True } ),
        ),
    "am looking for": (
        PTEntry( "seek", { voice.DRACONIAN: True } ),
        PTEntry( "iz lookin' fer", { voice.KITTEH: True } ),
        ),
    "anything":   (
        PTEntry( "stuff", { voice.STUPID: True } ),
        PTEntry( "anythin'", { voice.KITTEH: True } ),
        ),
    "ate":   (
        PTEntry( "eated", { voice.KITTEH: True, voice.SMART: False } ),
        PTEntry( "devoured", { voice.SMART: True } ),
        PTEntry( "consumed", { voice.DRACONIAN: True } ),
        ),
    "buy":   (
        PTEntry( "purchase", { voice.SMART: True } ),
        PTEntry( "buyz", { voice.KITTEH: True } ),
        PTEntry( "acquire", { voice.GNOMIC: True, voice.STUPID: False } ),
        PTEntry( "get", { voice.STUPID: True } ),
        ),
    "buy something":   (
        PTEntry( "trade" ),
        PTEntry( "get a thing", { voice.STUPID: True } ),
        PTEntry( "make a purchase", { voice.SMART: True } ),
        PTEntry( "lay down some coin", { voice.DWARVEN: True } ),
        PTEntry( "barter", { voice.DWARVEN: True } ),
        PTEntry( "haggle", { voice.GNOMIC: True } ),
        PTEntry( "barter", { voice.GNOMIC: True } ),
        PTEntry( "exchange treasures", { voice.DRACONIAN: True } ),
        PTEntry( "buy sum stuff", { voice.KITTEH: True } ),
        ),
    "Can I have":   (
        PTEntry( "I can haz", { voice.KITTEH: True, voice.SMART: False } ),
        ),
    "cat":   (
        PTEntry( "kitteh", { voice.KITTEH: True } ),
        ),
    'different':   (
        PTEntry( "divergent", { voice.SMART: True } ),
        PTEntry( "not the same", { voice.STUPID: True } ),
        PTEntry( "dissimilar", { voice.ELVEN: True } ),
        PTEntry( "difrunt", { voice.KITTEH: True } ),
        ),
    "Do you have":   (
        PTEntry( "You got", { voice.ORCISH: True } ),
        PTEntry( "You haz got", { voice.KITTEH: True, voice.SMART: False } ),
        ),
    "eternity":   (
        PTEntry( "eternitys", { voice.KITTEH: True } ),
        PTEntry( "all-tomorrows", { voice.DWARVEN: True } ),
        ),
    'exactly':   (
        PTEntry( "precisely", { voice.SMART: True } ),
        PTEntry( "perfectly", { voice.ELVEN: True } ),
        PTEntry( "right", { voice.STUPID: True } ),
        PTEntry( "egsaktly", { voice.KITTEH: True } ),
        PTEntry( "preshishley", { voice.KITTEH: True, voice.SMART: True } ),
        ),
    "forever":   (
        PTEntry( "furevur", { voice.KITTEH: True } ),
        ),
    "have":   (
        PTEntry( "'ave", { voice.ORCISH: True } ),
        PTEntry( "haves", { voice.DRACONIAN: True, voice.STUPID: True } ),
        PTEntry( "haz", { voice.KITTEH: True } ),
        ),
    "have .":   (
        PTEntry( "possess.", { voice.DRACONIAN: True } ),
        PTEntry( "haz.", { voice.KITTEH: True } ),
        ),
    "He":   (
        PTEntry( "Him", { voice.KITTEH: True, voice.STUPID: True } ),
        ),
    "he":   (
        PTEntry( "him", { voice.KITTEH: True, voice.STUPID: True } ),
        ),
    "Hello":   (
        PTEntry( "'Ello, ello", { voice.ORCISH: True } ),
        PTEntry( "'Ello", { voice.ORCISH: True, voice.STUPID: False } ),
        PTEntry( "Greetings", { voice.SMART: True } ),
        PTEntry( "Hey", { voice.STUPID: True } ),
        PTEntry( "Salutations", { voice.DRACONIAN: True, voice.STUPID: False } ),
        PTEntry( "Sss", { voice.DRACONIAN: True, voice.STUPID: True } ),
        PTEntry( "Hi", { voice.SMART: False, voice.DWARVEN: False, voice.ORCISH: False, voice.DRACONIAN: False } ),
        PTEntry( "Lali-ho", { voice.DWARVEN: True } ),
        PTEntry( "Hai", { voice.KITTEH: True } ),
        ),
    "Hello ,":   (
        PTEntry( "'Ello there,", { voice.ORCISH: True } ),
        PTEntry( "Greetingss,", { voice.DRACONIAN: True } ),
        PTEntry( "Lali-ho,", { voice.DWARVEN: True } ),
        PTEntry( "Oh hai there,", { voice.KITTEH: True } ),
        ),
    "here":   (
        PTEntry( "'ere", { voice.ORCISH: True } ),
        ),
    "hers":   (
        PTEntry( "her", { voice.KITTEH: True, voice.STUPID: True } ),
        PTEntry( "herz", { voice.KITTEH: True } ),
        ),
    "His":   (
        PTEntry( "Him", { voice.KITTEH: True, voice.STUPID: True } ),
        ),
    "his":   (
        PTEntry( "him", { voice.KITTEH: True, voice.STUPID: True } ),
        ),
    "I am": (
        PTEntry( "I'm" ),
        PTEntry( "I'z", { voice.KITTEH: True } ),
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
        PTEntry( "hard facts", { voice.DWARVEN: True } ),
        PTEntry( "informashun", { voice.KITTEH: True } ),
        PTEntry( "gnosis", { voice.GREEK: True } ),
       ),
    "is not": (
        PTEntry( "isn't" ),
        PTEntry( "ain't", { voice.STUPID: True } ),
        PTEntry( "izn't", { voice.KITTEH: True } ),
        ),
    "It is": (
        PTEntry( "It's" ),
        PTEntry( "It'z", { voice.KITTEH: True } ),
        ),
    "leader":   (
        PTEntry( "archon", { voice.GREEK: True } ),
        PTEntry( "boss", { voice.ORCISH: True } ),
        PTEntry( "bigwig", { voice.KITTEH: True } ),
        ),
    "Let me": (
        PTEntry( "Lemme", { voice.STUPID: True } ),
        PTEntry( "Allow me to", { voice.SMART: True } ),
        PTEntry( "I can", { voice.KITTEH: True } ),
        ),
    "little":   (
        PTEntry( "littul", { voice.KITTEH: True } ),
        PTEntry( "wee", { voice.KITTEH: True, voice.STUPID: False } ),
        ),
    "Looking for": (
        PTEntry( "Lookin' for", { voice.ORCISH: True } ),
        PTEntry( "Seeking", { voice.DRACONIAN: True } ),
        PTEntry( "Lookin fer", { voice.KITTEH: True } ),
        PTEntry( "In the market for", { voice.GNOMIC: True } ),
        ),
    "makes":   (
        PTEntry( "makez", { voice.KITTEH: True } ),
        ),
    "made":   (
        PTEntry( "maked", { voice.KITTEH: True, voice.SMART: False } ),
        PTEntry( "maded", { voice.KITTEH: True, voice.SMART: True } ),
        ),
    "me":   (
        PTEntry( "meh", { voice.KITTEH: True } ),
        ),
    "much":   (
        PTEntry( "mutch", { voice.KITTEH: True } ),
        PTEntry( "manys", { voice.KITTEH: True, voice.STUPID: True } ),
        ),
    "My":   (
        PTEntry( "Me", { voice.ORCISH: True } ),
        PTEntry( "Me", { voice.STUPID: True } ),
        PTEntry( "Mai", { voice.KITTEH: True } ),
        PTEntry( "Meh", { voice.KITTEH: True } ),
        ),
    "my":   (
        PTEntry( "me", { voice.ORCISH: True } ),
        PTEntry( "me", { voice.STUPID: True } ),
        PTEntry( "mai", { voice.KITTEH: True } ),
        PTEntry( "meh", { voice.KITTEH: True } ),
        ),
    "need":   (
        PTEntry( "needs", { voice.DRACONIAN: True } ),
        PTEntry( "needz", { voice.KITTEH: True } ),
        PTEntry( "require", { voice.STUPID: False } ),
        ),
    "no !":   (
        PTEntry( "noes!", { voice.KITTEH: True } ),
        ),
    "normal":   (
        PTEntry( "orthodox", { voice.GREEK: True } ),
        ),
    "nothing":   (
        PTEntry( "nuttin", { voice.KITTEH: True } ),
        ),
    "over":   (
        PTEntry( "ovah", { voice.KITTEH: True } ),
        ),
    "poison":   (
        PTEntry( "toxin", { voice.GREEK: True } ),
        ),
    "poisonous":   (
        PTEntry( "toxic", { voice.GREEK: True } ),
        ),
    "riddle":   (
        PTEntry( "enigma", { voice.GREEK: True } ),
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
        PTEntry( "lookit teh shinies", { voice.KITTEH: True } ),
        ),
    "She":   (
        PTEntry( "Her", { voice.KITTEH: True, voice.STUPID: True } ),
        ),
    "she":   (
        PTEntry( "her", { voice.KITTEH: True, voice.STUPID: True } ),
        ),
    "shop": (
        PTEntry( "store" ),
        PTEntry( "forge-front", { voice.DWARVEN: True } ),
        PTEntry( "boutique", { voice.ELVEN: True } ),
       ),
    "something": (
        PTEntry( "wotever", { voice.ORCISH: True } ),
        PTEntry( "somethin'", { voice.KITTEH: True } ),
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
        PTEntry( "Teh", { voice.KITTEH: True } ),
       ),
    "the": (
        PTEntry( "dat", { voice.ORCISH: True } ),
        PTEntry( "teh", { voice.KITTEH: True } ),
       ),
    "There": (
        PTEntry( "Thar", { voice.KITTEH: True } ),
        PTEntry( "Dere", { voice.ORCISH: True } ),
       ),
    "there": (
        PTEntry( "thar", { voice.KITTEH: True } ),
        PTEntry( "dere", { voice.ORCISH: True } ),
       ),
    "There is": (
        PTEntry( "There's" ),
        PTEntry( "Dere's", { voice.ORCISH: True } ),
        PTEntry( "Thar'z", { voice.KITTEH: True } ),
       ),
    "There is not": (
        PTEntry( "There isn't", { voice.STUPID: False } ),
        PTEntry( "There ain't", { voice.STUPID: True } ),
        PTEntry( "Dere ain't", { voice.ORCISH: True } ),
        PTEntry( "Dere ain't no", { voice.ORCISH: True, voice.STUPID: True } ),
        PTEntry( "Thar izn't", { voice.KITTEH: True, voice.STUPID: False } ),
        PTEntry( "Thar ain't", { voice.KITTEH: True, voice.STUPID: True } ),
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
        PTEntry( "Dis", { voice.KITTEH: True } ),
       ),
    "this": (
        PTEntry( "dis", { voice.ORCISH: True } ),
        PTEntry( "thiss", { voice.DRACONIAN: True } ),
        PTEntry( "dis", { voice.KITTEH: True } ),
       ),
    "This is": (
        PTEntry( "Dis ere's", { voice.ORCISH: True } ),
        PTEntry( "This here's", { voice.ORCISH: True, voice.SMART: True } ),
        PTEntry( "Dis are", { voice.KITTEH: True } ),
       ),
    "trying":   (
        PTEntry( "tryin", { voice.KITTEH: True, voice.STUPID: True } ),
        ),
    "want": (
        PTEntry( "desire", { voice.DRACONIAN: True } ),
        ),
    "wares": (
        PTEntry( "goods" ),
        PTEntry( "products", { voice.SMART: True } ),
        PTEntry( "shinies", { voice.KITTEH: True } ),
        ),
    "weak":   (
        PTEntry( "anemic", { voice.GREEK: True } ),
        PTEntry( "unfit", { voice.DRACONIAN: True } ),
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
        PTEntry( "O hai", { voice.KITTEH: True } ),
       ),
    "Welcome to": (
        PTEntry( "Git over ere to", { voice.ORCISH: True } ),
       ),
    "went":   (
        PTEntry( "goed", { voice.KITTEH: True } ),
        ),
    "what": (
        PTEntry( "wot", { voice.ORCISH: True } ),
        ),
    "wisdom":   (
        PTEntry( "philosophy", { voice.GREEK: True } ),
        ),
    "with":   (
        PTEntry( "wif", { voice.KITTEH: True } ),
        ),
    "Would": (
        PTEntry( "Wud", { voice.KITTEH: True } ),
        ),
    "would": (
        PTEntry( "wud", { voice.KITTEH: True } ),
        ),
    "would like": (
        PTEntry( "desire", { voice.DRACONIAN: True } ),
        PTEntry( "wantz", { voice.KITTEH: True } ),
        ),
    "your": (
        PTEntry( "yer", { voice.ORCISH: True } ),
        PTEntry( "youz", { voice.KITTEH: True } ),
        ),
    }
