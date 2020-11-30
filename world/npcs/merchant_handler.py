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
        footer = "==============================="
        