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

def return_rank_bonus(rank, difficulty):
    print(f"Entered Return Rank Bonus with rank: {rank} difficulty: {difficulty}")
    if difficulty == 'easy':
        rb = easy_rb
    elif difficulty == 'average':
        rb = average_rb
    elif difficulty == 'difficult':
        rb = difficult_rb
    elif difficulty == 'impossible':
        rb = impossible_rb

    rb = rb[rank - 1]
    return rb


def defense_layer_calc(char, only_skill_return=False, only_rb_return=False):
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
    TODO: Remove rank bonuses from character attributes and only ever dynamically produce them 
            based on the character's ranks, so that RB formula can always be changed later 
            without editing character attributes.

    High, Mid, and Low always refer to the area 
    of the body that the attack targets and not the numerical value.
    """

    b_defense_skill_list = []
    r_defense_skill_list = []
    l_defense_skill_list = []

    temp_rank = 0
    temp_difficulty = ''

    weap_high_skill, weap_mid_skill, weap_low_skill = '', '', ''
    offhand_high_skill, offhand_mid_skill, offhand_low_skill = '', '', ''
    dodge_high_skill, dodge_mid_skill, dodge_low_skill = '', '', ''

    # Initialize rankbonus values.
    weap_high_rb, weap_mid_rb, weap_low_rb = 0.0, 0.0, 0.0
    offhand_high_rb, offhand_mid_rb, offhand_low_rb = 0.0, 0.0, 0.0
    dodge_high_rb, dodge_mid_rb, dodge_low_rb = 0.0, 0.0, 0.0

    # Decide how many layers, based on if wielding.
    wielding = char.attributes.get('wielding')
    l_wield = wielding.get('left')
    r_wield = wielding.get('right')
    b_wield = wielding.get('both')


    if b_wield:
        if b_wield.attributes.has('skillset'):
            b_wield_skillset = b_wield.attributes.get('skillset')
            char_b_weap_skillset = char.attributes.get(b_wield_skillset) # Grab weapon skillset dictionary from char.
            skills = [*char_b_weap_skillset] # Create a list of the skill names.

            # Check each key in the dictionary against all viable skills.
            for i in skills:
                if skillsets[b_wield_skillset].get(i):
                    if skillsets[b_wield_skillset][i]['skill_type'] == 'defense':
                        b_defense_skill_list.append(i)

            # Sort 
            for i in b_defense_skill_list:
                temp_rank = char_b_weap_skillset.get(i)
                temp_difficulty = skillsets[b_wield_skillset][i]['difficulty']
                if skillsets[b_wield_skillset][i]['default_aim'] == 'high':
                    weap_high_rb += return_rank_bonus(temp_rank, temp_difficulty)
                    weap_high_skill = i
                elif skillsets[b_wield_skillset][i]['default_aim'] == 'mid':
                    weap_mid_rb += return_rank_bonus(temp_rank, temp_difficulty)
                    weap_mid_skill = i
                elif skillsets[b_wield_skillset][i]['default_aim'] == 'low':
                    weap_low_rb += return_rank_bonus(temp_rank, temp_difficulty)
                    weap_low_skill = i

    if r_wield:
        if r_wield.attributes.has('skillset'):
            r_wield_skillset = r_wield.attributes.get('skillset')
            char_r_weap_skillset = char.attributes.get(r_wield_skillset) # Grab weapon skillset dictionary from char.
            skills = [*char_r_weap_skillset] # Create a list of the skill names.

            # Check each key in the dictionary against all viable skills.
            for i in skills:
                if skillsets[r_wield_skillset].get(i):
                    if skillsets[r_wield_skillset][i]['skill_type'] == 'defense':
                        r_defense_skill_list.append(i)

            for i in r_defense_skill_list:
                temp_rank = char_r_weap_skillset.get(i)
                temp_difficulty = skillsets[r_wield_skillset][i]['difficulty']
                if skillsets[r_wield_skillset][i]['default_aim'] == 'high':
                    weap_high_rb += char_r_weap_skillset[i].get('rank_bonus')
                    weap_high_skill = i
                elif skillsets[r_wield_skillset][i]['default_aim'] == 'mid':
                    weap_mid_rb += char_r_weap_skillset[i].get('rank_bonus')
                    weap_mid_skill = i
                elif skillsets[r_wield_skillset][i]['default_aim'] == 'low':
                    weap_low_rb += char_r_weap_skillset[i].get('rank_bonus')
                    weap_low_skill = i

    if l_wield:
        if l_wield.is_typeclass('typeclasses.objects.Shields'):
            if l_wield.attributes.has('skillset'):
                l_wield_skillset = l_wield.attributes.get('skillset')
                char_l_weap_skillset = char.attributes.get(l_wield_skillset) # Grab weapon skillset dictionary from char.
                skills = [*char_l_weap_skillset] # Create a list of the skill names.

                # Check each key in the dictionary against all viable skills.
                for i in skills:
                    if skillsets[l_wield_skillset].get(i):
                        if skillsets[l_wield_skillset][i]['skill_type'] == 'defense':
                            l_defense_skill_list.append(i)

                for i in l_defense_skill_list:
                    temp_rank = char_b_weap_skillset.get(i)
                    temp_difficulty = skillsets[b_wield_skillset][i]['difficulty']
                    if skillsets[l_wield_skillset][i]['default_aim'] == 'high':
                        offhand_high_rb += char_l_weap_skillset[i].get('rank_bonus')
                        offhand_high_skill = i
                    elif skillsets[l_wield_skillset][i]['default_aim'] == 'mid':
                        offhand_mid_rb += char_l_weap_skillset[i].get('rank_bonus')
                        offhand_mid_skill = i
                    elif skillsets[l_wield_skillset][i]['default_aim'] == 'low':
                        offhand_low_rb += char_l_weap_skillset[i].get('rank_bonus')
                        offhand_low_skill = i
        else:
            if l_wield.attributes.has('skillset'):
                l_wield_skillset = l_wield.attributes.get('skillset')
                char_l_weap_skillset = char.attributes.get(l_wield_skillset) # Grab weapon skillset dictionary from char.
                skills = [*char_l_weap_skillset] # Create a list of the skill names.

                # Check each key in the dictionary against all viable skills.
                for i in skills:
                    if skillsets[l_wield_skillset].get(i):
                        if skillsets[l_wield_skillset][i]['skill_type'] == 'defense':
                            l_defense_skill_list.append(i)

                for i in l_defense_skill_list:
                    temp_rank = char_l_weap_skillset.get(i)
                    temp_difficulty = skillsets[l_wield_skillset][i]['difficulty']
                    if skillsets[l_wield_skillset][i]['default_aim'] == 'high':
                        offhand_high_rb += char_l_weap_skillset[i].get('rank_bonus')
                        offhand_high_skill = i
                    elif skillsets[l_wield_skillset][i]['default_aim'] == 'mid':
                        offhand_mid_rb += char_l_weap_skillset[i].get('rank_bonus')
                        offhand_mid_skill = i
                    elif skillsets[l_wield_skillset][i]['default_aim'] == 'low':
                        offhand_low_rb += char_l_weap_skillset[i].get('rank_bonus')
                        offhand_low_skill = i

    # Get all dodge rank bonuses
    # !!! NO DODGES EXIST YET !!!
    
    high_skills = [weap_high_skill, offhand_high_skill, dodge_high_skill]
    mid_skills = [weap_mid_skill, offhand_mid_skill, dodge_mid_skill]
    low_skills = [weap_low_skill, offhand_low_skill, dodge_low_skill]
    
    # High Layer
    h_rb = [weap_high_rb, dodge_high_rb, offhand_high_rb]
    h_rb.sort(reverse=True)
    h_layer1 = h_rb[0] * 1
    h_layer2 = h_rb[1] * 0.5
    h_layer3 = h_rb[2] * 0.33
    high_def_rb = (h_layer1 + h_layer2 + h_layer3)

    # Mid Layer
    m_rb = [weap_mid_rb, dodge_mid_rb, offhand_mid_rb]
    m_rb.sort(reverse=True)
    m_layer1 = m_rb[0] * 1
    m_layer2 = m_rb[1] * 0.5
    m_layer3 = m_rb[2] * 0.33
    mid_def_rb = (m_layer1 + m_layer2 + m_layer3)

    # Low Layer
    l_rb = [weap_low_rb, dodge_low_rb, offhand_low_rb]
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

    if only_skill_return:
        return high_skills, mid_skills, low_skills
    elif only_rb_return:
        return high_def_rb, mid_def_rb, low_def_rb
    else:
        return high_skills, mid_skills, low_skills, high_def_rb, mid_def_rb, low_def_rb

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
    staves = {'total_ranks': 300, 'leg_sweep': 100, 'end_jab': 100, 'high_block': 100}
    '''
    # Return the data of the skill.
    difficulty = skillsets[skillset][skill]['difficulty']
    
    # Check if the skillset is not already learned and if not, create it.
    if not char.attributes.has(skillset):
        char.attributes.add(skillset, {'total_ranks': 0})

    dic_skillset = char.attributes.get(skillset)

    # Check if the skill already exists. Create it otherwise. 
    if not dic_skillset.get(skill):
        dic_skillset[skill] = 0
    rank = dic_skillset[skill]
    rank += 1
    dic_skillset[skill] = rank
    dic_skillset['total_ranks'] += 1
    char.msg(f"You learn rank {rank} of {skillset} {skill}, earning the rank bonus of {return_rank_bonus(rank, difficulty)}.")


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
    skill_rank = 0
    skill_rank_bonus = 0.0
    skill_difficulty = ''

    total_ranks = 0
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

        if char.attributes.get(i): # If the skillset exists on the character.
            skillset_dic = char.attributes.get(i) # Store that skillset's dictionary.
            total_ranks = skillset_dic.get('total_ranks')

            # Build skill lists
            for x in VIABLE_SKILLS:
                if skillset_dic.get(x): # If the skill exists on the character.
                    skill_rank = skillset_dic.get(x) # Store that skill's dictionary.
                    skill_difficulty = skillsets[i][x]['difficulty']
                    skill_rank_bonus = return_rank_bonus(skill_rank, skill_difficulty)

                    # Store the skill's name in a list, sorted by skill type.
                    if skillsets[i][x]['skill_type'] == 'offense':
                        offense_skill_list.append(x)
                        offense_rank_list.append(skill_rank)
                        offense_rank_bonus_list.append(skill_rank_bonus)
                    elif skillsets[i][x]['skill_type'] == 'defense':
                        defense_skill_list.append(x)
                        defense_rank_list.append(skill_rank)
                        defense_rank_bonus_list.append(skill_rank_bonus)
                    elif skillsets[i][x]['skill_type'] == 'utility':
                        utility_skill_list.append(x)
                        utility_rank_list.append(skill_rank)
                        utility_rank_bonus_list.append(skill_rank_bonus)

            # Build this skillset's string.
            skillset_title = (f"\n\n|g{cap(i)}|n - Total Ranks: |g{total_ranks}|n\n"
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

    # Current total defensive rank bonuses.
    high_def_rb, mid_def_rb, low_def_rb = defense_layer_calc(char, only_rb_return=True)
    def_rb = f"\n\nCurrent total defensive RB - High: {high_def_rb}    Mid: {mid_def_rb}    Low: {low_def_rb}\n"

    result = f"{header}{full_skillsets_string}{def_rb}\n{footer}"
    return result