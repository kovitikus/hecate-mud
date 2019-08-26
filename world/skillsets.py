
def skill_level(rank, difficulty):
    '''
    RANK += RANK BONUS PER RANK
    --------------------------
    1 to 10 += 3
    11 to 30 += 2
    31 to 50 += 1
    51 to 100 += 0.5
    101 to 150 += 0.25
    151 to 200 += 0.125
    201 to 500 += 0.0625
    501 to 1,000 += 0.025
    1,001 to infinity += 0.01
    '''
    rb = 0

    #Formula
    if rank:
        r = rank if rank < 10 else 10
        rb += (3 * r)
        if rank >= 11:
            r = rank - 10 if rank < 30 else 10
            rb += (2 * r)
            if rank >= 31:
                r = rank - 30 if rank < 50 else 20
                rb += (1 * r)
                if rank >= 51:
                    r = rank - 50 if rank < 100 else 50
                    rb += (0.5 * r)
                    if rank >= 101:
                        r = rank - 100 if rank < 150 else 50
                        rb += (0.25 * r)
                        if rank >= 151:
                            r = rank - 150 if rank < 200 else 50
                            rb += (0.125 * r)
                            if rank >= 201:
                                r = rank - 200 if rank < 500 else 300
                                rb += (0.0625 * r)
                                if rank >= 501:
                                    r = rank - 500 if rank < 1000 else 500
                                    rb += (0.025 * r)
                                    if rank >= 1001:
                                        r = rank - 1000
                                        rb += (0.01 * r)
        '''
        15% RB loss per difficulty. 
        At rank 100:
        Easy(100%) 115 RB
        Average(85%) 97.75 RB
        Difficult(70%) 80.5 RB
        Impossible(55%) 63.25 RB
        '''
        if difficulty == 'easy':
            rb *= 1
        elif difficulty == 'average':
            rb *= 0.85
        elif difficulty == 'difficult':
            rb *= 0.7
        elif difficulty == 'impossible':
            rb *= 0.55
        return rb # Return if any rank.
    return None # Return if no rank.

def defense_layer_calc(char, skillset):
        """
        Defensive rank bonus includes up to 3 layers of defense.
        The highest RB defensive manuever of each high, mid, and low will gain 100% of it's RB.
        The second highest RB will supply 50% and the third will only be worth 33%.
        Each layer can only consist of a single defensive manuever from each of the following categories:
            Weapon Blocks, Combat Manuever Dodges, and Shield Blocks.
            Weapons that require 2 hands can only ever gain 2 defensive layers. Shields are the only way to gain all 3 layers.

        For Example:
        Staves Mid Block with 100 Rank Bonus * 1 = 100
        CM Mid Dodge with 80 Rank Bonus * 0.5 = 40
        Total Mid Defensive Rank Bonus = 140

        Swords Mid Block with 100 Rank Bonus * 0.33 = 33
        CM Mid Dodge with 150 Rank Bonus * 0.5 = 75
        Shield Mid Block with 200 Rank Bonus * 1 = 200
        Total Mid Defensive Rank Bonus = 308

        Floats are used to determine the highest RB priority, but only rounded down integers are used to determine the total RB.

        TODO: Add a round down for the final RB.

        High, Mid, and Low always refer to the area 
        of the body that the attack targets and not the numerical value.
        """

        """Weapon Rank Bonus"""
        weap_dic = char.db.def_skills.get('weapon')
        weap_high_def = weap_dic.get('high')
        weap_mid_def = weap_dic.get('mid')
        weap_low_def = weap_dic.get('low')
        weap_high_rb = 0.0
        weap_mid_rb = 0.0
        weap_low_rb = 0.0

        if weap_high_def.get(skillset):
            weap_high_dic = weap_high_def.get(skillset)
            weap_high_dic_values = weap_high_dic.values()
            for rb in weap_high_dic_values:
                if rb > weap_high_rb:
                    weap_high_rb = rb

        if weap_mid_def.get(skillset):
            weap_mid_dic = weap_mid_def.get(skillset)
            weap_mid_dic_values = weap_mid_dic.values()
            for rb in weap_mid_dic_values:
                if rb > weap_mid_rb:
                    weap_mid_rb = rb

        if weap_low_def.get(skillset):
            weap_low_dic = weap_low_def.get(skillset)
            weap_low_dic_values = weap_low_dic.values()
            for rb in weap_low_dic_values:
                if rb > weap_low_rb:
                    weap_low_rb = rb
        

        """Dodge Rank Bonus"""
        dodge_dic = char.db.def_skills.get('dodge')
        dodge_high_def = dodge_dic.get('high')
        dodge_mid_def = dodge_dic.get('mid')
        dodge_low_def = dodge_dic.get('low')
        dodge_high_rb = 0.0
        dodge_mid_rb = 0.0
        dodge_low_rb = 0.0

        if dodge_high_def.get('cm'):
            dodge_high_dic = dodge_high_def.get('cms')
            dodge_high_dic_values = dodge_high_dic.values()
            for rb in dodge_high_dic_values:
                if rb > dodge_high_rb:
                    dodge_high_rb = rb

        if dodge_mid_def.get('cm'):
            dodge_mid_dic = dodge_mid_def.get('cms')
            dodge_mid_dic_values = dodge_mid_dic.values()
            for rb in dodge_mid_dic_values:
                if rb > dodge_mid_rb:
                    dodge_mid_rb = rb

        if dodge_low_def.get('cm'):
            dodge_low_dic = dodge_low_def.get('cms')
            dodge_low_dic_values = dodge_low_dic.values()
            for rb in dodge_low_dic_values:
                if rb > dodge_low_rb:
                    dodge_low_rb = rb

    
        """Shield Rank Bonus"""
        shield_dic = char.db.def_skills.get('shield')
        shield_high_def = shield_dic.get('high')
        shield_mid_def = shield_dic.get('mid')
        shield_low_def = shield_dic.get('low')
        shield_high_rb = 0.0
        shield_mid_rb = 0.0
        shield_low_rb = 0.0

        if shield_high_def.get('shield'):
            shield_high_dic = shield_high_def.get('shield')
            shield_high_dic_values = shield_high_dic.values()
            for rb in shield_high_dic_values:
                if rb > shield_high_rb:
                    shield_high_rb = rb

        if shield_mid_def.get('shield'):
            shield_mid_dic = shield_mid_def.get('shield')
            shield_mid_dic_values = shield_mid_dic.values()
            for rb in shield_mid_dic_values:
                if rb > shield_mid_rb:
                    shield_mid_rb = rb

        if shield_low_def.get('shield'):
            shield_low_dic = shield_low_def.get('shield')
            shield_low_dic_values = shield_low_dic.values()
            for rb in shield_low_dic_values:
                if rb > shield_low_rb:
                    shield_low_rb = rb


        """
        Calculate Layering
        First Highest RB gets 100%
        Second Highest RB gets 50%
        Third Highest RB gets 33%
        """

        """High Layer"""
        # weap_high_rb, dodge_high_rb, shield_high_rb
        h_rb = [weap_high_rb, dodge_high_rb, shield_high_rb]
        h_rb.sort(reverse=True)
        h_layer1 = h_rb[0] * 1
        h_layer2 = h_rb[1] * 0.5
        h_layer3 = h_rb[2] * 0.33
        high_def_rb = (h_layer1 + h_layer2 + h_layer3)

        """Mid Layer"""
        # weap_mid_rb, dodge_mid_rb, shield_mid_rb
        m_rb = [weap_mid_rb, dodge_mid_rb, shield_mid_rb]
        m_rb.sort(reverse=True)
        m_layer1 = m_rb[0] * 1
        m_layer2 = m_rb[1] * 0.5
        m_layer3 = m_rb[2] * 0.33
        mid_def_rb = (m_layer1 + m_layer2 + m_layer3)

        """Low Layer"""
        # weap_low_rb, dodge_low_rb, shield_low_rb
        l_rb = [weap_low_rb, dodge_low_rb, shield_low_rb]
        l_rb.sort(reverse=True)
        l_layer1 = l_rb[0] * 1
        l_layer2 = l_rb[1] * 0.5
        l_layer3 = l_rb[2] * 0.33
        low_def_rb = (l_layer1 + l_layer2 + l_layer3)

        # Assign the values to the character.
        def_rb = char.db.def_rb
        def_rb['high'] = high_def_rb
        def_rb['mid'] = mid_def_rb
        def_rb['low'] = low_def_rb

def rb_stance(self, o_rb, d_rb, stance):
    '''
    o_rb = Offensive Rank Bonus
    d_rb = Defensive Rank Bonus

    Berserk - Attack 100% | Defense: 0%
    Aggressive - Attack 75% | Defense: 25%
    Normal - Attack 50% | Defense: 50%
    Wary - Attack 25% | Defense: 75%
    Defensive - Attack 0% | Defense: 100%
    '''
    if stance == 'berserk':
        o_rb = o_rb * 1
        d_rb = d_rb * 0
        return o_rb, d_rb
    if stance == 'aggressive':
        o_rb = o_rb * 0.75
        d_rb = d_rb * 0.25
        return o_rb, d_rb
    if stance == 'normal':
        o_rb = o_rb * 0.5
        d_rb = d_rb * 0.5
        return o_rb, d_rb
    if stance == 'wary':
        o_rb = o_rb * 0.25
        d_rb = d_rb * 0.75
        return o_rb, d_rb
    if stance == 'defensive':
        o_rb = o_rb * 0
        d_rb = d_rb * 1
        return o_rb, d_rb

easy_rb = []
average_rb = []
difficult_rb = []
impossible_rb = []

for i in range(1, 1_001):
    rb = skill_level(i, 'easy')
    easy_rb.append(rb)

    rb = skill_level(i, 'average')
    average_rb.append(rb)

    rb = skill_level(i, 'difficult')
    difficult_rb.append(rb)

    rb = skill_level(i, 'impossible')
    impossible_rb.append(rb)

# Skillsets
skillsets = {'staves': 
                {'leg sweep': 
                    {'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low'},
                'feint': 
                    {'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low'},
                'end jab': 
                    {'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'swat': 
                    {'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'simple strike': 
                    {'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'side strike': 
                    {'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'pivot smash': 
                    {'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'longarm strike': 
                    {'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'simple block': 
                    {'damage_type': 'weapon_block', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': ['mid', 'low']},
                'cross block': 
                    {'damage_type': 'weapon_block', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': ['mid', 'low']},
                'overhead block': 
                    {'damage_type': 'weapon_block', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': ['high']},
                'parting jab': 
                    {'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'parting swat': 
                    {'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'parting smash':
                     {'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'defensive sweep': 
                    {'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low'},
                'stepping spin': 
                    {'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'snapstrike': 
                    {'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'sweep strike': 
                    {'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': ['low', 'high']},
                'spinstrike': 
                    {'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'tbash': 
                    {'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'whirling block': 
                    {'damage_type': 'weapon_block', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': ['high']},
                'pivoting longarm': 
                    {'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'}
                },
            'holy':
                {'heal':
                    {'damage_type': 'heal', 'difficulty': 'average', 'hands': 0, 'attack_range': 'either', 'default_aim': 'mid'}
                }
            }

# Create lists of the skillsets and their skills.
VIABLE_SKILLSETS = []
VIABLE_SKILLS = []
temp_skill_list = []
for k, v in skillsets.items():
    VIABLE_SKILLSETS.append(k)
    temp_skill_list.append(v)
for i in temp_skill_list:
    for k, v in i.items():
        VIABLE_SKILLS.append(k)
    

def learn_skill(char, skillset, skill):
    '''
    Skill Difficulty = Skill Point Cost per Rank
    ---------------------------------------------

    Easy = 5
    Average = 7
    Difficult = 9
    Impossible = 11

    Example Skillset Saved Attribute
    ---------------------------------
    staves = {'total_sp': 125, 'total_ranks': 500, 'leg_sweep': {'rank': 100, 'rb': 115}, 'feint': {'rank': 100', 'rb': 115}, 'end_jab': {'rank':100, rb: }}

    '''
    # Return the data of the skill.
    gsp = char.attributes.get('gsp')

    difficulty = skillsets[skillset][skill]['difficulty']
    
    # Set the per rank SP cost and rank bonus dictionary of the skill.
    sp_cost = 0
    if difficulty == 'easy':
        rb = easy_rb
        sp_cost = 5
    elif difficulty == 'average':
        rb = average_rb
        sp_cost = 7
    elif difficulty == 'difficult':
        rb = difficult_rb
        sp_cost = 9
    elif difficulty == 'impossible':
        rb = impossible_rb
        sp_cost = 11
    
    # Check if the skillset is not already learned and if not, create it.
    if not char.attributes.has(skillset):
        #Check for general skill points required to learn.
        if not gsp >= sp_cost:
            char.msg('You do not have enough general skill points to learn this skillset.')
            return
        char.attributes.add(skillset, {'total_sp': sp_cost, 'total_ranks': 0})
        char.db.gsp -= sp_cost

    d_skillset = char.attributes.get(skillset)
    total_sp = d_skillset['total_sp']
    if not total_sp >= sp_cost:
        char.msg('You do not have enough skill points to learn this skill.')
        return
    if not d_skillset.get(skill):
        d_skillset[skill] = {'rank': 0, 'rb': 0}
    rank = d_skillset[skill]['rank']
    rank += 1
    d_skillset[skill]['rank'] = rank
    d_skillset['total_sp'] -= sp_cost
    rb = rb[rank - 1]
    d_skillset[skill]['rb'] = rb
    d_skillset['total_ranks'] += 1
    char.msg(f"You have spent {sp_cost} SP to learn rank {rank} of {skillset} {skill}, earning the rank bonus of {d_skillset[skill]['rb']}.")



    # Setup the defensive skill attributes for High, Mid, Low defensive layering calculations.
    d_skill = skillsets[skillset][skill]
    def_a = d_skill.get('default_aim')
    damage_type = d_skill['damage_type']
    def_skills = char.attributes.get('def_skills')

    for d_a in def_a:
        if damage_type == 'weapon_block':
            if not skillset in def_skills:
                def_skills['weapon'][d_a] = {skillset: None}
                if not skill in def_skills:
                    def_skills['weapon'][d_a][skillset] = {skill: None}
            def_skills['weapon'][d_a][skillset][skill] = rb
    
        elif damage_type == 'dodge':
            if not skillset in def_skills:
                def_skills['weapon'][d_a] = {skillset: None}
                if not skill in def_skills:
                    def_skills['weapon'][d_a][skillset] = {skill: None}
            def_skills['weapon'][d_a][skillset][skill] = rb

        elif damage_type == 'shield_block':
            if not skillset in def_skills:
                def_skills['weapon'][d_a] = {skillset: None}
                if not skill in def_skills:
                    def_skills['weapon'][d_a][skillset] = {skill: None}
            def_skills['weapon'][d_a][skillset][skill] = rb

    defense_layer_calc(char, skillset)