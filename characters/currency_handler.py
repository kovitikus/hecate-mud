class CurrencyHandler:
    def __init__(self, owner):
        self.owner = owner

    def return_coin_string(self):
        owner = self.owner
        if owner.attributes.has('coin'):
            coin_dict = owner.attributes.get('coin')
            return self.all_coin_to_string(self, coin_dict)

    def return_each_coin(self):
        coin_dict = dict(self.owner.attributes.get('coin'))
        return coin_dict['plat'], coin_dict['gold'], coin_dict['silver'], coin_dict['copper']

    def all_coin_to_string(self, coin_dict):
        """
        Converts all coin elements into a string, no matter their value.

        Arguments:
            coin_dict (dictionary): A dictionary consisting of all 4 coin types.
        Returns:
            (string): The resulting string.
        """
        return f"{coin_dict['plat']}p {coin_dict['gold']}g {coin_dict['silver']}s {coin_dict['copper']}c"

    def positive_coin_to_string(self, coin_dict):
        """
        Converts only the coin elements that are greater than 0 into a string.

        Arguments:
            coin_dict (dictionary): A dictionary consisting of all 4 coin types.
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
        return f"{plat}{gold}{silver}{copper}"

    def add_coin_to_owner(self, added_coin_dict):
        owner = self.owner
        original_coin_dict = owner.attributes.get('coin', None)
        if original_coin_dict:
            owner.db.coin = self.add_coin(original_coin_dict, added_coin_dict) 

    def add_coin(self, original_coin_dict, added_coin_dict):
        """
        Adds one coin dictionary to another, then balances the results to maintain a maximum
        of 999 in each coin.

        Arguments:
            original_coin_dict (dict): The original coin values.
            added_coin_dict (dict): The dictionary of coin to add to original.

        Returns:
            (dict): The added and balanced coin dictionary.
        """
        for k in original_coin_dict:
            original_coin_dict[k] += added_coin_dict[k]
        return self.balance_coin(original_coin_dict)

    def subtract_coin_from_owner(self, subtracted_coin_dict):
        owner = self.owner
        current_coin_dict = owner.attributes.get('coin', default=None)
        if current_coin_dict:
            owner.db.coin = self.subtract_coin(current_coin_dict, subtracted_coin_dict)

    def subtract_coin(self, original_coin_dict, subtracted_coin_dict):
        original_copper = self.convert_coin_dict_to_copper(original_coin_dict)
        subtracted_copper = self.convert_coin_dict_to_copper(subtracted_coin_dict)
        result_copper = original_copper - subtracted_copper
        return self.balance_coin(self.generate_coin_dict(copper=result_copper))

    def multiply_coin(self, coin_dict, multiplier):
        """
        Takes a coin dictionary and multiplies each value by a multiplier.
        Balances the result and returns it.

        Arguments:
            coin_dict (dict): The dictionary of coins to multiply.
            multiplier (int): The multiplier to use on the coins.

        Returns:
            coin_dict (dict): The resulting multiplied and balanced coin dictionary.
        """
        copper = self.convert_coin_dict_to_copper(coin_dict)
        result_copper = copper * multiplier
        return self.balance_coin(self.generate_coin_dict(copper=result_copper))

    def greater_or_equal_coin(self, original_coin_dict, comparison_coin_dict):
        original_copper = self.convert_coin_dict_to_copper(original_coin_dict)
        comparison_copper = self.convert_coin_dict_to_copper(comparison_coin_dict)
        return original_copper >= comparison_copper

    

    def convert_coin_dict_to_copper(self, coin_dict):
        copper = 0
        for coin_type, amount in coin_dict.items():
            copper += self.convert_coin(**{coin_type:amount})
        return copper

    def balance_coin(self, coin_dict):
        """
        Takes a coin dictionary and balances all coins to a maximum of 999, pushing the
        remainder up to the next coin type.

        Arguments:
            coin_dict (dictionary): {'plat': value, 'gold': value, 'silver': value, 'copper': value}
        
        Returns:
            coin_dict (dictionary): {'plat': value, 'gold': value, 'silver': value, 'copper': value}
        """
        plat, gold, silver, copper = self.return_each_coin(coin_dict)

        if copper > 999:
            silver += int(self.convert_coin(copper=copper, result_type=silver))
            copper = 999

        if silver > 999:
            gold += int(self.convert_coin(silver=silver, result_type=gold))
            silver = 999
        
        if gold > 999:
            plat += int(self.convert_coin(gold=gold, result_type=plat))
            gold = 999

        return {'plat': plat, 'gold': gold, 'silver': silver, 'copper': copper}

    def convert_coin(self, plat=0, gold=0, silver=0, copper=0, result_type='copper'):
        """
        Converts any number of coin types into a single type of coin.
        For example, it can convert 25 gold and 35 plat and result in a total amount of copper.
        (Don't worry about how much copper that is. It's what this method is for!)

        Keyword Arguments:
            plat (int): Amount of platinum to convert.
            gold (int): Amount of gold to convert.
            silver (int): Amount of silver to convert.
            coppper (int): Amount of copper to convert.
            result_type (string): The type of coin the result should be. Defaults to copper.
        """
        if result_type == 'plat':
            return (copper / 1_000_000_000) + (silver / 1_000_000) + (gold / 1_000) + plat
        elif result_type == 'gold':
            return (copper / 1_000_000) + (silver / 1_000) + gold + (plat * 1_000)
        elif result_type == 'silver':
            return (copper / 1_000) + silver + (gold * 1_000) + (plat * 1_000_000)
        else: # result_type == copper
            return copper + (silver * 1_000) + (gold * 1_000_000) + (plat * 1_000_000_000)

    def generate_coin_dict(self, plat=0, gold=0, silver=0, copper=0):
        return {'plat': plat, 'gold': gold, 'silver': silver, 'copper': copper}
