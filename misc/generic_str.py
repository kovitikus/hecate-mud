cap = str.capitalize
vowels = ['a', 'e', 'i', 'o', 'u']

consonant_vowels = ['amazigh', 'euboean', 'eucharist', 'eumenides', 'eurasian', 'euro-american', 'europe', 
'european', 'eusebius', 'oaxaca', 'ouija', 'ucalegon', 'uclaf', 'udale', 
'udall', 'udy', 'ueberroth', 'uganda', 'uinita', 'ukase', 'ukie', 'ukraine', 'ukrainian', 'ullyses', 'unakas', 
'uniate', 'unix', 'uranus', 'usanian', 'usonian', 'utah', 'utahn', 'utonian', 'esclop', 'eucalyptus', 'eucatastrophe', 
'euchologion', 'euchre', 'euclidianness', 'eudaemon', 'eudemonia', 'eugarie', 'eugenesis', 'eugenics', 'eugenist', 
'eugeny', 'euglena', 'eukaryote', 'eulachon', 'eulogy', 'eunoia', 'eunuch', 'euouae', 'euphemism', 'euphoria', 
'euphoriant', 'eureka', 'euro', 'eustasy', 'eustress', 'eutectic', 'euth', 'euthanasia', 'eutripsia', 'ewe', 'ewer', 
'latmul', 'once', 'oncer', 'one', 'onesie', 'ouabain', 'ubac', 'uberty', 'ubication', 'ubicity', 'ubiety', 'ubiquity', 
'udometer', 'uey', 'ufo', 'ufologist', 'ufology', 'uke', 'ukelele', 'ukulele', 'ululate', 'ululation', 'unanimity', 
'unanimous', 'unary', 'uni', 'unicameral', 'unicorn', 'unicycle', 'unidirection', 'unidirectional', 'unidirectionality', 
'uniform', 'uniformitarianism', 'unify', 'unigeniture', 'union', 'unique', 'uniquity', 'unisex', 'unison', 'unit', 'unite', 
'unity', 'univalence', 'univalent', 'universalism', 'universe', 'university', 'univocal', 'upas', 'upsilon', 'uraeus', 
'ural', 'uranism', 'uranist', 'uranium', 'uranophobia', 'urea', 'ureter', 'ureteroureterostomy', 'urethra', 'uridine', 
'urinal', 'urinalysis', 'urine', 'urology', 'uropygium', 'urus', 'usability', 'usage', 'use', 'user', 'using', 'usual', 
'usufruct', 'usufruction', 'usufructuary', 'usurer', 'usuress', 'usurp', 'usurper', 'usurping', 'usury', 'ute', 'utensil', 
'uterus', 'utile', 'utilitarian', 'utility', 'utopia', 'utopographer', 'utricle', 'uvarovite', 'uvas', 'uvea', 'uvula', 
'uvular', 'zzxjoanw']

def article(word):
    word.lower()
    if word in consonant_vowels:
        article = 'a'
    elif word[0] in vowels:
        article = 'an'
    elif word in consonant_vowels:
        article = 'a'
    else:
        article = 'a'
    return article

def pronoun(char):
    if not char.attributes.has('figure'):
        possessive = 'its'
        singular_subject = 'it'
        singular_object = 'it'
    elif char.db.figure['gender'] == 'male':
        possessive = 'his'
        singular_subject = 'he'
        singular_object = 'him'
    elif char.db.figure['gender'] == 'female':
        possessive = 'hers'
        singular_subject = 'she'
        singular_object = 'her'
    return possessive, singular_subject, singular_object

def proper_name(char):
    if not char.attributes.has('figure'):
        name = char.key
    elif char.db.figure['gender'] == 'male' or 'female':
        name = cap(char.key)
    return name

def possessive(string):
    """
    Determines whether to place an 's or just an ' at the end of a string, to represent possession.

    Arguments:
        string (string): The string to evaluate.
    
    Returns:
        string (string): The final result with the attached possession.
    """
    if string[-1] == 's':
        string = f"{string}\'"
    else:
        string = f"{string}'s"
    return string
