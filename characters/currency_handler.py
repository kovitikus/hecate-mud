class CurrencyHandler:
    def __init__(self, owner):
        self.owner = owner

    def return_currency(self, owner):
        if owner.attributes.has('coin'):
            coin_dic = owner.attributes.get('coin')
            string = f"{coin_dic['plat']}p {coin_dic['gold']}g {coin_dic['silver']}s {coin_dic['copper']}c"
            return string

    def return_obj_coin(self, obj):
        if obj.attributes.has('coin'):
            return obj.db.coin['plat'], obj.db.coin['gold'], obj.db.coin['silver'], obj.db.coin['copper']

    def add_coin(self, owner, plat=0, gold=0, silver=0, copper=0):
        if owner.attributes.has('coin'):
            coin_dic = owner.attributes.get('coin')
            plat_dic = coin_dic['plat']
            gold_dic = coin_dic['gold']
            silver_dic = coin_dic['silver']
            copper_dic = coin_dic['copper']
        
            total_copper = copper + copper_dic
            total_silver = silver + silver_dic
            total_gold = gold + gold_dic
            total_plat = plat + plat_dic

            if total_copper > 999:
                total_silver += int(self.convert_coin(copper=total_copper, result_type=silver))
                total_copper = 999

            if total_silver > 999:
                total_gold += int(self.convert_coin(silver=total_silver, result_type=gold))
                total_silver = 999
            
            if total_gold > 999:
                total_plat += int(self.convert_coin(gold=total_gold, result_type=plat))
                total_gold = 999

            coin_dic['copper'] = total_copper
            coin_dic['silver'] = total_silver
            coin_dic['gold'] = total_gold
            coin_dic['plat'] = total_plat

    def remove_coin(self, owner, plat=0, gold=0, silver=0, copper=0):
        if owner.attributes.has('coin'):
            coin_dic = owner.attributes.get('coin')
            plat_dic = coin_dic['plat']
            gold_dic = coin_dic['gold']
            silver_dic = coin_dic['silver']
            copper_dic = coin_dic['copper']

            total_copper = copper_dic - copper
            total_silver = silver_dic - silver
            total_gold = gold_dic - gold
            total_plat = plat_dic - plat

            if total_copper > 999:
                total_silver += int(self.convert_coin(copper=total_copper, result_type=silver))
                total_copper = 999

            if total_silver > 999:
                total_gold += int(self.convert_coin(silver=total_silver, result_type=gold))
                total_silver = 999
            
            if total_gold > 999:
                total_plat += int(self.convert_coin(gold=total_gold, result_type=plat))
                total_gold = 999

            coin_dic['copper'] = total_copper
            coin_dic['silver'] = total_silver
            coin_dic['gold'] = total_gold
            coin_dic['plat'] = total_plat

    def convert_coin(self, plat=0, gold=0, silver=0, copper=0, result_type='copper'):
        if result_type == 'plat':
            plat = (copper / 1_000_000_000) + (silver / 1_000_000) + (gold / 1_000)
            return plat

        elif result_type == 'gold':
            gold = (copper / 1_000_000) + (silver / 1_000) + (plat * 1_000)
            return gold
            
        elif result_type == 'silver':
            silver = (copper / 1_000) + (gold * 1_000) + (plat * 1_000_000)
            return silver
            
        else:
            copper = (silver * 1_000) + (gold * 1_000_000) + (plat * 1_000_000_000)
            return copper
