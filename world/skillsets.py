from evennia.utils.utils import list_to_string


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

def best_weap_def(char, skillset):
    weap_dic = char.db.def_skills.get('weapon')
    weap_high_def = weap_dic.get('high')
    weap_mid_def = weap_dic.get('mid')
    weap_low_def = weap_dic.get('low')
    weap_high_rb = 0.0
    weap_mid_rb = 0.0
    weap_low_rb = 0.0
    best_weap_high_skill = None
    best_weap_mid_skill = None
    best_weap_low_skill = None

    if weap_high_def.get(skillset):
        weap_high_dic = weap_high_def.get(skillset)
        print(weap_high_dic)
        for k, v in weap_high_dic.items():
            if v > weap_high_rb:
                best_weap_high_skill = k
                weap_high_rb = v
        weap_high_dic['best_weap_high_skill'] = best_weap_high_skill

    if weap_mid_def.get(skillset):
        weap_mid_dic = weap_mid_def.get(skillset)
        for k, v in weap_mid_dic.items():
            if v > weap_mid_rb:
                best_weap_mid_skill = k
                weap_mid_rb = v
        weap_mid_dic['best_weap_mid_skill'] = best_weap_mid_skill

    if weap_low_def.get(skillset):
        weap_low_dic = weap_low_def.get(skillset)
        for k, v in weap_low_dic.items():
            if v > weap_low_rb:
                best_weap_low_skill = k
                weap_low_rb = v
        weap_low_dic['best_weap_low_skill'] = best_weap_low_skill

    return weap_high_rb, weap_mid_rb, weap_low_rb

def best_dodge_def(char, skillset):
    dodge_dic = char.db.def_skills.get('dodge')
    dodge_high_def = dodge_dic.get('high')
    dodge_mid_def = dodge_dic.get('mid')
    dodge_low_def = dodge_dic.get('low')
    dodge_high_rb = 0.0
    dodge_mid_rb = 0.0
    dodge_low_rb = 0.0
    best_dodge_high_skill = None
    best_dodge_mid_skill = None
    best_dodge_low_skill = None

    if dodge_high_def.get('cm'):
        dodge_high_dic = dodge_high_def.get('cms')
        for k, v in dodge_high_dic.items():
            if v > dodge_high_rb:
                best_dodge_high_skill = k
                dodge_high_rb = v
        dodge_high_dic['best_dodge_high_skill'] = best_dodge_high_skill

    if dodge_mid_def.get('cm'):
        dodge_mid_dic = dodge_mid_def.get('cms')
        for k, v in dodge_mid_dic.items():
            if v > dodge_mid_rb:
                best_dodge_mid_skill = k
                dodge_mid_rb = v
        dodge_mid_dic['best_dodge_mid_skill'] = best_dodge_mid_skill

    if dodge_low_def.get('cm'):
        dodge_low_dic = dodge_low_def.get('cms')
        for k, v in dodge_low_dic.items():
            if v > dodge_low_rb:
                best_dodge_low_skill = k
                dodge_low_rb = v
        dodge_low_dic['best_dodge_low_skill'] = best_dodge_low_skill

    return dodge_high_rb, dodge_mid_rb, dodge_low_rb

def best_shield_def(char, skillset):
    shield_dic = char.db.def_skills.get('shield')
    shield_high_def = shield_dic.get('high')
    shield_mid_def = shield_dic.get('mid')
    shield_low_def = shield_dic.get('low')
    shield_high_rb = 0.0
    shield_mid_rb = 0.0
    shield_low_rb = 0.0
    best_shield_high_skill = None
    best_shield_mid_skill = None
    best_shield_low_skill = None

    if shield_high_def.get('shield'):
        shield_high_dic = shield_high_def.get('shield')
        for k, v in shield_high_dic.items():
            if v > shield_high_rb:
                best_shield_high_skill = k
                shield_high_rb = v
        shield_high_dic['best_shield_high_skill'] = best_shield_high_skill

    if shield_mid_def.get('shield'):
        shield_mid_dic = shield_mid_def.get('shield')
        for k, v in shield_mid_dic.items():
            if v > shield_mid_rb:
                best_shield_mid_skill = k
                shield_mid_rb = v
        shield_mid_dic['best_shield_mid_skill'] = best_shield_mid_skill

    if shield_low_def.get('shield'):
        shield_low_dic = shield_low_def.get('shield')
        for k, v in shield_low_dic.items():
            if v > shield_low_rb:
                best_shield_low_skill = k
                shield_low_rb = v
        shield_low_dic['best_shield_low_skill'] = best_shield_low_skill

    return shield_high_rb, shield_mid_rb, shield_low_rb

def defense_layer_calc(char):
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

        # weap_high_rb, weap_mid_rb, weap_low_rb = best_weap_def(char, skillset)
        # dodge_high_rb, dodge_mid_rb, dodge_low_rb = best_dodge_def(char, skillset)
        # shield_high_rb, shield_mid_rb, shield_low_rb = best_shield_def(char, skillset)

        # Initialize rankbonus values.
        weap_high_rb, weap_mid_rb, weap_low_rb = 0, 0, 0
        shield_high_rb, shield_mid_rb, shield_low_rb = 0, 0 ,0
        dodge_high_rb, dodge_mid_rb, dodge_low_rb = 0, 0, 0

        # Decide how many layers, based on if wielding.
        wielding = char.attributes.get('wielding')
        l_wield = wielding.get('left')
        r_wield = wielding.get('right')
        b_wield = wielding.get('both')


        if b_wield:
            if b_wield.attributes.get('skillset'):
                b_weapon_skillset = char.b_wield.attributes.get('skillset') # Grab weapon skillset dictionary from char.
                dic_defense = b_weapon_skillset.get('defense') # Grab defensive skills dictioanry.
                skills = dic_defense.keys() # Create a list of the defensive skill names.
    
                for i in skills:
                    if skillsets[b_weapon_skillset][i]['default_aim'] == 'high':
                        weap_high_rb += dic_defense.get(i)
                    elif skillsets[b_weapon_skillset][i]['default_aim'] == 'mid':
                        weap_mid_rb += dic_defense.get(i)
                    elif skillsets[b_weapon_skillset][i]['default_aim'] == 'low':
                        weap_low_rb += dic_defense.get(i)


        if r_wield:
            if r_wield.attributes.get('skillset'):
                r_weapon_skillset = r_wield.attributes.get('skillset')
                dic_defense = r_weapon_skillset.get('defense') # Grab defensive skills dictioanry.
                skills = dic_defense.keys() # Create a list of the defensive skill names.
    
                for i in skills:
                    if skillsets[r_weapon_skillset][i]['default_aim'] == 'high':
                        weap_high_rb += dic_defense.get(i)
                    elif skillsets[r_weapon_skillset][i]['default_aim'] == 'mid':
                        weap_mid_rb += dic_defense.get(i)
                    elif skillsets[r_weapon_skillset][i]['default_aim'] == 'low':
                        weap_low_rb += dic_defense.get(i)

        if l_wield.is_typeclass('typeclasses.objects.Shields'):
            if l_wield.attributes.get('skillset'):
                shield_skillset = l_wield.attributes.get('skillset')
                dic_defense = shield_skillset.get('defense') # Grab defensive skills dictioanry.
                skills = dic_defense.keys() # Create a list of the defensive skill names.
    
                for i in skills:
                    if skillsets[shield_skillset][i]['default_aim'] == 'high':
                        weap_high_rb += dic_defense.get(i)
                    elif skillsets[shield_skillset][i]['default_aim'] == 'mid':
                        weap_mid_rb += dic_defense.get(i)
                    elif skillsets[shield_skillset][i]['default_aim'] == 'low':
                        weap_low_rb += dic_defense.get(i)
        elif l_wield:
            if l_wield.attributes.get('skillset'):
                l_weapon_skillset = l_wield.attributes.get('skillset')
                dic_defense = l_weapon_skillset.get('defense') # Grab defensive skills dictioanry.
                skills = dic_defense.keys() # Create a list of the defensive skill names.
    
                for i in skills:
                    if skillsets[l_weapon_skillset][i]['default_aim'] == 'high':
                        weap_high_rb += dic_defense.get(i)
                    elif skillsets[l_weapon_skillset][i]['default_aim'] == 'mid':
                        weap_mid_rb += dic_defense.get(i)
                    elif skillsets[l_weapon_skillset][i]['default_aim'] == 'low':
                        weap_low_rb += dic_defense.get(i)

        
        
        

        # High Layer
        h_rb = [weap_high_rb, dodge_high_rb, shield_high_rb]
        h_rb.sort(reverse=True)
        h_layer1 = h_rb[0] * 1
        h_layer2 = h_rb[1] * 0.5
        h_layer3 = h_rb[2] * 0.33
        high_def_rb = (h_layer1 + h_layer2 + h_layer3)

        # Mid Layer
        m_rb = [weap_mid_rb, dodge_mid_rb, shield_mid_rb]
        m_rb.sort(reverse=True)
        m_layer1 = m_rb[0] * 1
        m_layer2 = m_rb[1] * 0.5
        m_layer3 = m_rb[2] * 0.33
        mid_def_rb = (m_layer1 + m_layer2 + m_layer3)

        # Low Layer
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

# Skillset Order: Alphabetically
# Skill Order: Offensive, Defensive, Utility > Difficulty > Alphabetically
skillsets = {'staves': 
                {'end jab': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'parting jab': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'parting swat': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'simple strike': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'swat': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'parting smash':
                     {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'pivot smash': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'side strike': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'snapstrike': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'stepping spin': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'longarm strike': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'pivoting longarm': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'spinstrike': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'sweep strike': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': ['low', 'high']},
                'tbash': 
                    {'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'mid block': 
                    {'skill_type': 'defense', 'damage_type': None, 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'},
                'low block': 
                    {'skill_type': 'defense', 'damage_type': None, 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low'},
                'overhead block': 
                    {'skill_type': 'defense', 'damage_type': None, 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'defensive sweep': 
                    {'skill_type': 'utility', 'damage_type': None, 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low'},
                'feint': 
                    {'skill_type': 'utility', 'damage_type': None, 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low'},
                'leg sweep': 
                    {'skill_type': 'utility', 'damage_type': None, 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low'}
                },
            'holy':
                {'heal':
                    {'skill_type': 'utility', 'damage_type': 'heal', 'difficulty': 'average', 'hands': 0, 'attack_range': 'either', 'default_aim': 'mid'}
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
    staves = {'total_sp': 125, 'total_ranks': 500, 'offense': {'leg_sweep': {'rank': 100, 'rank_bonus': 115}, 'end_jab': {'rank': 100, 'rank_bonus': }, 'defense': {'high_block': etc, etc}}
    '''
    # Return the data of the skill.
    difficulty = skillsets[skillset][skill]['difficulty']
    skill_type = skillsets[skillset][skill]['skill_type']
    
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
        char.attributes.add(skillset, {'total_sp': sp_cost, 'total_ranks': 0})

    dic_skillset = char.attributes.get(skillset)
    total_sp = dic_skillset['total_sp']
    if total_sp < sp_cost:
        char.msg('You do not have enough skill points to learn this skill.')
        return
    
    # # Place skill in either attack or defense dictionary, based on damage type.
    # if skill_type == 'defense':
    #     #place skill in defense category
    #     dic_type = dic_skillset.get('defense')
    # elif skill_type == 'offense':
    #     #place skill in attack category
    #     dic_type = dic_skillset.get('offense')

    # Check if the skill already exists. Create it otherwise. 
    if not dic_skillset.get(skill):
        dic_skillset[skill] = {'rank': 0, 'rank_bonus': 0}
    rank = dic_skillset[skill]['rank']
    rank += 1
    dic_skillset[skill]['rank'] = rank
    dic_skillset['total_sp'] -= sp_cost
    rb = rb[rank - 1]
    dic_skillset[skill]['rank_bonus'] = rb
    dic_skillset['total_ranks'] += 1
    char.msg(f"You have spent {sp_cost} SP to learn rank {rank} of {skillset} {skill}, earning the rank bonus of {dic_skillset[skill]['rank_bonus']}.")



    # # Setup the defensive skill attributes for High, Mid, Low defensive layering calculations.
    # d_skill = skillsets[skillset][skill]
    # def_a = d_skill.get('default_aim')
    # damage_type = d_skill['damage_type']
    # if not char.attributes.has('def_skills'):
    #         char.attributes.add('def_skills', {'weapon': {'high': {}, 'mid': {}, 'low': {}}, 'dodge': {'high': {}, 'mid': {}, 'low': {}}, 'shield': {'high': {}, 'mid': {}, 'low': {}}})
    # def_skills = char.attributes.get('def_skills')

    # for d_a in def_a:
    #     if damage_type == 'weapon_block':
    #         if not skillset in def_skills:
    #             def_skills['weapon'][d_a] = {skillset: None}
    #             if not skill in def_skills:
    #                 def_skills['weapon'][d_a][skillset] = {skill: None}
    #         def_skills['weapon'][d_a][skillset][skill] = rb
    
    #     elif damage_type == 'dodge':
    #         if not skillset in def_skills:
    #             def_skills['weapon'][d_a] = {skillset: None}
    #             if not skill in def_skills:
    #                 def_skills['weapon'][d_a][skillset] = {skill: None}
    #         def_skills['weapon'][d_a][skillset][skill] = rb

    #     elif damage_type == 'shield_block':
    #         if not skillset in def_skills:
    #             def_skills['weapon'][d_a] = {skillset: None}
    #             if not skill in def_skills:
    #                 def_skills['weapon'][d_a][skillset] = {skill: None}
    #         def_skills['weapon'][d_a][skillset][skill] = rb

    # defense_layer_calc(char, skillset)


def generate_skill_list(char):
    """
    Desired Outcome

    =====[Skills]=====================================

    {skillset_name}
    -------------------------------
    Offense:
    {skill_name}            Rank: {rank}        Rank Bonus: {rank_bonus}

    Defense:

    ==================================================
    """
    cap = str.capitalize

    offense_skill_list = []
    defense_skill_list = []
    utility_skill_list = []

    offense_rank_list = []
    defense_rank_list = []
    utility_rank_list = []
    
    offense_rank_bonus_list = []
    defense_rank_bonus_list = []
    utility_rank_bonus_list = []

    offense_skill_string_list = []
    defense_skill_string_list = []
    utility_skill_string_list = []

    skillset_string_list = []

    skillset_dic = None
    skill_dic = None

    total_ranks = 0
    skill_points = 0.0
    num = 0
    offense_skill_string = ""
    defense_skill_string = ""
    utility_skill_string = ""
    full_skillsets_string = ""

    header = "=====[|gSkills|n]====================================="
    footer = "=================================================="

  
    for i in VIABLE_SKILLSETS:
        # We reset the skill lists at the start of each new skillset iteration.
        offense_skill_list = []
        defense_skill_list = []
        utility_skill_list = []

        offense_rank_list = []
        defense_rank_list = []
        utility_rank_list = []

        offense_rank_bonus_list = []
        defense_rank_bonus_list = []
        utility_rank_bonus_list = []

        offense_skill_string_list = []
        defense_skill_string_list = []
        utility_skill_string_list = []

        offense_skill_string = ''
        defense_skill_string = ''
        utility_skill_string = ''

        if char.attributes.get(i): # If the skillset exists on the character.
            skillset_dic = char.attributes.get(i) # Store that skillset's dictionary.
            total_ranks = skillset_dic.get('total_ranks')
            skill_points = skillset_dic.get('total_sp')

            # Build skill lists
            for x in VIABLE_SKILLS:
                if skillset_dic.get(x): # If the skill exists on the character.
                    skill_dic = skillset_dic.get(x) # Store that skill's dictionary.

                    # Store the skill's name in a list, sorted by skill type.
                    if skillsets[i][x]['skill_type'] == 'offense':
                        offense_skill_list.append(x)
                        offense_rank_list.append(skill_dic['rank'])
                        offense_rank_bonus_list.append(skill_dic['rank_bonus'])
                    elif skillsets[i][x]['skill_type'] == 'defense':
                        defense_skill_list.append(x)
                        defense_rank_list.append(skill_dic['rank'])
                        defense_rank_bonus_list.append(skill_dic['rank_bonus'])
                    elif skillsets[i][x]['skill_type'] == 'utility':
                        utility_skill_list.append(x)
                        utility_rank_list.append(skill_dic['rank'])
                        utility_rank_bonus_list.append(skill_dic['rank_bonus'])

            # Build this skillset's string.
            skillset_title = (f"\n\n|g{cap(i)}|n - Skill Points: |g{skill_points}|n    Total Ranks: |g{total_ranks}|n\n"
                        "--------------------------------------------------")
            num = 0
            for v in offense_skill_list:
                offense_skill_string_list.append(f"|G{cap(v)}|n            Rank: |G{offense_rank_list[num]}|n        RB: |G{offense_rank_bonus_list[num]}|n\n")
                num += 1
            if len(offense_skill_string_list) > 0:
                offense_skill_string = f"\nOffense:\n{''.join(offense_skill_string_list)}"

            num = 0
            for v in defense_skill_list:
                defense_skill_string_list.append(f"|G{cap(v)}|n            Rank: |G{defense_rank_list[num]}|n        RB: |G{defense_rank_bonus_list[num]}|n\n")
                num += 1
            if len(defense_skill_string_list) > 0:
                defense_skill_string = f"\nDefense:\n{''.join(defense_skill_string_list)}"

            num = 0
            for v in utility_skill_list:
                utility_skill_string_list.append(f"|G{cap(v)}|n            Rank: |G{utility_rank_list[num]}|n        RB: |G{utility_rank_bonus_list[num]}|n\n")
                num += 1
            if len(utility_skill_string_list) > 0:
                utility_skill_string = f"\nUtility:\n{''.join(utility_skill_string_list)}"
            
            skillset_string_list.append(f"{skillset_title}{offense_skill_string}{defense_skill_string}{utility_skill_string}")

    # Now we compile the final list.
    full_skillsets_string = ''.join(skillset_string_list)
    result = f"{header}{full_skillsets_string}\n{footer}"
    return result