from evennia.prototypes.spawner import spawn
from evennia.utils.evtable import EvTable, EvCell

from misc import general_mechanics as gen_mec
from misc import generic_str

class MerchantHandler:
    def __init__(self, owner):
        self.owner = owner

    def list_stock(self):
        """
        Uses the stock attribute on the merchant (owner) to display a list of items available
        for purchase.

        Returns:
            (string): An error message or the resulting stock listing.
        """
        owner = self.owner
        owner_possessive = generic_str.possessive(owner.key)
        stocked_items = owner.attributes.get('stock', default=None)
        if not stocked_items:
            return f"{owner.key} currently has no stock!"

        header = EvCell(f"[{owner_possessive} Stock]", align='c', width=25, fill_char='=')
        stock_table = EvTable(border=None, pad_width=0)
        footer = EvCell("", align='c', width=25, fill_char='=')

        for item, properties in stocked_items.items():
            # Stock is manually added to the merchant. This should always have at least 1 result.
            proto_dict_list = gen_mec.prototype_to_dictionary(item)
            if len(proto_dict_list) > 0:
                proto_dict = proto_dict_list[0]
            else:
                # The prototype for this stock item couldn't be found, abandon it.
                continue

            item_name = proto_dict.get('key')
            price_str = owner.currency.positive_coin_types_to_string(coin_dict=proto_dict.get('price'))
            quantity = properties.get('quantity', 0)

            stock_table.add_row(f"{item_name} ", f"Price: {price_str}", f"Qty: {quantity}")

        stock_table.reformat_column(0, fill_char='.')
        stock_table.reformat_column(1, pad_left=1, fill_char='.')
        stock_table.reformat_column(2, pad_left=1)

        return f"{header}\n{stock_table}{footer}"
            
    def sell_item(self, buyer, item, quantity=1):
        """
        Enables a character to purchase items from this merchant (owner).

        Arguments:
            buyer (Character): The character object that requested to purchase an item.
            item (string): The user input for the requested item.

        Keyword Arguments:
            quantity (int): The number of items requested. Defaults to 1 if not set.

        Returns:
            (string): The resulting message. Either an error explaining why the purchase can't be
                made or the details of a successful sale.
        """
        owner = self.owner

        # Confirm that the merchant has stock.
        stocked_items = owner.attributes.get('stock', default=None)
        if not stocked_items:
            return f"{owner.name} has no stock for sale."

        # Confirm that the buyer has a coin dictionary.
        buyer_coin_dict = buyer.attributes.get('coin', default=None)
        if not buyer_coin_dict:
            return "You don't have any coin."
        else:
            buyer_copper = buyer.currency.coin_dict_to_copper(buyer_coin_dict)

        potential_prototype_list = gen_mec.prototype_to_dictionary(item) # Returns a list of dictionaries.
        prototype_dict = None

        # Check each potential prototype result and compare it to the merchant's stock
        # to find an exact matching result.
        for prototype in potential_prototype_list:
            if prototype['key'] in stocked_items.keys():
                prototype_dict = prototype
                break
        if not prototype_dict:
            return f"{owner.name} is not selling {item}!"

        # Get the item name and its price from the prototype dictionary.
        item = prototype_dict['key']
        price_dict = prototype_dict.get('price', None)
        if not price_dict: # TODO: Add error logging here, including a mail sent to the admin.
            return f"|rERROR! The price for {item} could not be found! Please report this to the admin.|n"
        else:
            copper_price = owner.currency.coin_dict_to_copper(price_dict)

        # Check to make sure that the merchant has the item in stock, in the requested quantity.
        if stocked_items[item]['quantity'] <= 0:
            return f"{item} is out of stock!"
        elif stocked_items[item]['quantity'] < quantity:
            return f"{owner.name} does haven't {quantity} of {item} in stock!"

        total_copper_price = copper_price * quantity
        total_price_dict = owner.currency.copper_to_coin_dict(total_copper_price)
        total_price_str = owner.currency.positive_coin_types_to_string(coin_dict=total_price_dict)

        # Check if the player has enough money
        if buyer_copper > total_copper_price:
            buyer_copper -= total_copper_price
            buyer.db.coin = buyer.copper_to_coin_dict(buyer_copper)
        else:
            return f"You do not possess {total_price_str} to make that purchase!"

        stocked_items[item] -= quantity
        for _ in range(quantity):
            spawned_item = spawn(item)[0]
            spawned_item.move_to(owner.location, quiet=True)
        purchase_str = (f"You buy {quantity} of {item} for a total of {total_price_str}. "
                        f"{owner.name} places them in the room.")
        return purchase_str
