from world.items import item_prototypes
from world.general_mechanics import return_proto_attr_dic, return_proto_key

class MerchantHandler:
    def __init__(self, owner):
        self.owner = owner

    def return_stock(self):
        """
        =========[Stock]===============
        a poorly-crafted torch
        an unappetizing food ration
        a dirty flask of oil
        a crude iron lantern
        a make-shift fishing rod
        a piece of foul-smelling bait
        ===============================
        """
        owner = self.owner
        if owner.attributes.has('stock'):
            stocked_items = owner.attributes.get('stock')

        header = "=========[Stock]==============="
        body = []
        footer = "==============================="
        item = None
        name = None
        price = None

        for i in stocked_items:
            name = return_proto_key(i)
            attr_dic = return_proto_attr_dic(i)
            price = attr_dic.get('price', 0)
            body.append(f"{name}    {price}\n")

        msg = f"{header}\n{''.join(body)}{footer}"
        return msg
            
        