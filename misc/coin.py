from evennia.prototypes.spawner import spawn

def return_all_coin_types(coin_dict):
    """
    Takes a coin dictionary and returns the value of all 4 types of coins, as individual variables.

    If a coin dictionary is not provided, the method attempts to pull one from the owner object.
    If that fails, a coin dictionary is created with all 0 values.

    Keyword Arguments:
        coin_dict (dict): A dictionary of coins and their values.

    Returns:
        plat (int): The value of platinum coin.
        gold (int): The value of gold coin.
        silver (int): The value of silver coin.
        copper (int): The value of copper coin.
    """
    return coin_dict['plat'], coin_dict['gold'], coin_dict['silver'], coin_dict['copper']

def all_coin_types_to_string(coin_dict):
    """
    Converts all coin elements into a string, no matter their value.

    Keyword Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.

    Returns:
        (string): The resulting string.
    """
    return f"{coin_dict['plat']}p {coin_dict['gold']}g {coin_dict['silver']}s {coin_dict['copper']}c"

def positive_coin_types_to_string(coin_dict):
    """
    Converts only the coin elements that are greater than 0 into a string.

    Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.

    Returns:
        (string): The resulting string.
    """
    plat = ""
    gold = ""
    silver = ""
    copper = ""
    if coin_dict['plat'] > 0:
        plat = f"{coin_dict['plat']}p "
    if coin_dict['gold'] > 0:
        gold = f"{coin_dict['gold']}g "
    if coin_dict['silver'] > 0:
        silver = f"{coin_dict['silver']}s "
    if coin_dict['copper'] > 0:
        copper = f"{coin_dict['copper']}c"
    return f"{plat}{gold}{silver}{copper}".strip()

def balance_coin_dict(coin_dict):
    """
    Takes a coin dictionary and balances all coins in excess of 999.
    Pushes the quotient of 1,000 up to the next coin type and leaves the remainder.

    Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.

    Returns:
        coin_dict (dict): A dictionary consisting of all 4 coin types.
    """
    def quotient(value):
        return value // 1_000
    def remainder(value):
        return value % 1_000

    plat, gold, silver, copper = return_all_coin_types(coin_dict=coin_dict)

    if copper > 999:
        silver += quotient(copper)
        copper = remainder(copper)

    if silver > 999:
        gold += quotient(silver)
        silver = remainder(silver)
    
    if gold > 999:
        plat += quotient(gold)
        gold = remainder(gold)

    return create_coin_dict(plat=plat, gold=gold, silver=silver, copper=copper)

def convert_coin_type(plat=0, gold=0, silver=0, copper=0, result_type='copper'):
    """
    Converts any number of coin types into a single type of coin.
    For example, it can convert 585433 copper + 35 plat into silver.
    (Don't worry about how much silver that is. It's what this method is for!)

    Converting upward will likely result in a float, whereas only converting downward
    will always result in an integer. This is critical information to keep in mind when
    using this method.

    Keyword Arguments:
        plat (int): Amount of platinum to convert.
        gold (int): Amount of gold to convert.
        silver (int): Amount of silver to convert.
        coppper (int): Amount of copper to convert.
        result_type (string): The type of coin the result should be. Defaults to copper.

    Returns:
        plat (int) or (float)
        gold (int) or (float)
        silver (int) or (float)
        coppper (int) or (float)
    """
    def convert_upward(current_tier_amount):
        return current_tier_amount / 1_000
    def convert_downward(current_tier_amount):
        return current_tier_amount * 1_000

    if result_type == 'plat':
        silver += convert_upward(copper)
        gold += convert_upward(silver)
        plat += convert_upward(gold)
        return plat
    elif result_type == 'gold':
        silver += convert_upward(copper)
        gold += convert_upward(silver)
        gold += convert_downward(plat)
        return gold
    elif result_type == 'silver':
        silver += convert_upward(copper)
        gold += convert_downward(plat)
        silver += convert_downward(gold)
        return silver
    else: # result_type == copper
        gold += convert_downward(plat)
        silver += convert_downward(gold)
        copper += convert_downward(silver)
        return copper

def create_coin_dict(plat=0, gold=0, silver=0, copper=0):
    """
    Creates a new dictionary with all 4 coin types.
    Any coin type that doesn't have a value passed to this method defaults to 0.

    Keyword Arguments:
        plat (int): The value of platinum coin.
        gold (int): The value of gold coin.
        silver (int): The value of silver coin.
        copper (int): The value of copper coin.
    Returns:
        coin_dict (dict): A dictionary consisting of all 4 coin types. 
    """
    return {'plat': plat, 'gold': gold, 'silver': silver, 'copper': copper}

def coin_dict_to_copper(coin_dict):
    """
    Converts a coin dictionary down to a total amount of copper.

    Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.

    Returns:
        copper (int): The total copper value of the coin dictionary.
    """
    return convert_coin_type(**coin_dict)

def copper_to_coin_dict(copper):
    """
    Takes any amount of coppper and converts it into a dictionary with that same
    amount of copper.
    It then balances the dictionary, pushing values above 999 up to the next coin type.

    Arguments:
        copper (int): The amount of copper to convert into a coin dictionary.

    Returns:
        coin_dict (dict): A dictionary consisting of all 4 coin types.
    """
    return balance_coin_dict(create_coin_dict(copper=copper))

def is_homogenized(coin_dict):
    """
    Checks a coin dictionary to find out if there's only 1 type of coin with a value above 0.

    Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.
    
    Returns:
        is_homogenized (boolean): True or False
    """
    num = 0
    for coin_value in coin_dict.values():
        if coin_value > 0:
            num += 1
    if num > 1:
        return False
    else:
        return True

def generate_coin_object(coin_dict=None, copper=None):
    """
    Determines what type of coin object and key to generate based on the coin dictionary.

    Keyword Arguments:
        coin_dict (dict): A dictionary consisting of all 4 coin types.
        copper (integer): A value representing the total amount of coin.

    Returns:
        coin_obj (object): The final spawned object, with its key properly set.
    """
    if copper is not None:
        coin_dict = copper_to_coin_dict(copper)
    elif coin_dict is None and copper is None:
        coin_dict = create_coin_dict()
        # A coin must have some sort of value, therefore generate a single copper coin.
        coin_dict['copper'] = 1

    homogenized = is_homogenized(coin_dict)
    coin_prototype = None
    pluralized = False

    if homogenized:
        for coin_type, coin_value in coin_dict.items():
            if coin_value > 0:
                coin_prototype = f"{coin_type}_coin"
            if coin_value > 1:
                pluralized = True
    else:
        coin_prototype = 'coin_pile'

    coin_obj = spawn(coin_prototype)[0]
    coin_obj.db.coin = coin_dict

    if pluralized:
        coin_obj.key = f"a pile of {coin_obj.db.plural_key}"

    return coin_obj
