from evennia.prototypes.spawner import spawn
from world.items import item_prototypes
from world.general_mechanics import return_proto_dic

class MerchantHandler:
    def __init__(self, owner):
        self.owner = owner

    def return_stock(self):
        # Example stock.
        """
        =========[Stock]===============
        a poorly-crafted torch    Price: 4c    Qty: 50
        an unappetizing food ration    Price: 10c    Qty: 25
        a dirty flask of oil    Price: 20c    Qty: 25
        a crude iron lantern    Price: 100c    Qty: 5
        a make-shift fishing rod    Price: 15c    Qty: 10
        a piece of foul-smelling bait    Price: 1c    Qty: 100
        ===============================
        """
        owner = self.owner
        if owner.attributes.has('stock'):
            stocked_items = owner.attributes.get('stock')

        header = "=========[Stock]==============="
        body = []
        footer = "==============================="
        name = None
        price = None
        quantity = 0

        for k, v in stocked_items.items():
            item_dic = return_proto_dic(k)

            name = item_dic.get('key')
            price = item_dic.get('price', 0)
            quantity = v

            body.append(f"{name}    Price: {price}c    Qty: {quantity}\n")

        msg = f"{header}\n{''.join(body)}{footer}"
        return msg
            
    def sell_item(self, buyer, item, quantity=1):
        owner = self.owner
        if owner.attributes.has('stock'):
            stocked_items = owner.attributes.get('stock')
        
        if item not in stocked_items.keys():
            msg = f"{owner.name} is not selling {item}!"
        elif stocked_items[item] <= 0:
            msg = f"{item} is out of stock!"
        elif stocked_items[item] < quantity:
            msg = f"{owner.name} does haven't {quantity} of {item} in stock!"
        else:
            # get the price of the item
            item_dic = return_proto_dic(item)
            price = item_dic['price']

            # multiply it by the quantity
            total_price = price * quantity

            # Check if the player has enough money
            coin_shortage = f"You do not possess {total_price}c to make that purchase!"
            if buyer.attributes.has('coin'):
                buyer_coin = buyer.attributes.get('coin')
                buyer_copper = buyer_coin.get('copper', 0)
                if buyer_copper < total_price:
                    return coin_shortage
                else:
                    buyer_coin['copper'] -= total_price
            else:
                return coin_shortage

            stocked_items[item] -= quantity
            msg = f"You buy {quantity} of {item} for a total of {total_price}. {owner.name} places them in the room."
            for _ in range(quantity):
                spawned_item = spawn(item)[0]
                # spawned_item = spawned_item[0]
                spawned_item.move_to(owner.location, quiet=True)
        return msg
