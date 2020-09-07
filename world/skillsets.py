def generate_rank_score(rank, difficulty):
    '''
    RANK += rank score PER RANK
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
    rs = 0

    #Formula
    if rank:
        r = rank if rank < 10 else 10
        rs += (3 * r)
        if rank >= 11:
            r = rank - 10 if rank < 30 else 10
            rs += (2 * r)
            if rank >= 31:
                r = rank - 30 if rank < 50 else 20
                rs += (1 * r)
                if rank >= 51:
                    r = rank - 50 if rank < 100 else 50
                    rs += (0.5 * r)
                    if rank >= 101:
                        r = rank - 100 if rank < 150 else 50
                        rs += (0.25 * r)
                        if rank >= 151:
                            r = rank - 150 if rank < 200 else 50
                            rs += (0.125 * r)
                            if rank >= 201:
                                r = rank - 200 if rank < 500 else 300
                                rs += (0.0625 * r)
                                if rank >= 501:
                                    r = rank - 500 if rank < 1000 else 500
                                    rs += (0.025 * r)
                                    if rank >= 1001:
                                        r = rank - 1000
                                        rs += (0.01 * r)
        '''
        15% RS loss per difficulty. 
        At rank 100:
        Easy(100%) 115 RS
        Average(85%) 97.75 RS
        Difficult(70%) 80.5 RS
        Impossible(55%) 63.25 RS
        '''
        if difficulty == 'easy':
            rs *= 1
        elif difficulty == 'average':
            rs *= 0.85
        elif difficulty == 'difficult':
            rs *= 0.7
        elif difficulty == 'impossible':
            rs *= 0.55
        return rs # Return if any rank.
    return None # Return if no rank.

easy_rs = []
average_rs = []
difficult_rs = []
impossible_rs = []

for i in range(1, 1_001):
    rs = generate_rank_score(i, 'easy')
    easy_rs.append(rs)

    rs = generate_rank_score(i, 'average')
    average_rs.append(rs)

    rs = generate_rank_score(i, 'difficult')
    difficult_rs.append(rs)

    rs = generate_rank_score(i, 'impossible')
    impossible_rs.append(rs)


def generate_ap():
    ap_granted = 1
    # Here is where modifiers will kick in, such as rolling for the chance at extra AP.
    return ap_granted

def ap_required(desired_rank):
    ap_per_rank = 100
    count = 0
    for _ in range(2, desired_rank+1):
        count += 1
        if count == 20:
            ap_per_rank += 10
            count = 0
    return ap_per_rank


# Skillset Order: Alphabetically
# Skill Order: Offensive, Defensive, Utility > Difficulty > Alphabetically
skillsets = {'martial arts':
                {'dodge':
                    {'uid': 'marts dodge','skill_type': 'defense', 'damage_type': None, 'difficulty': 'easy', 'hands': 0, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': None},
                'duck':
                    {'uid': 'marts duck','skill_type': 'defense', 'damage_type': None, 'difficulty': 'easy', 'hands': 0, 'attack_range': 'either', 'default_aim': 'high', 'weapon': None},
                'jump':
                    {'uid': 'marts jump','skill_type': 'defense', 'damage_type': None, 'difficulty': 'easy', 'hands': 0, 'attack_range': 'either', 'default_aim': 'low', 'weapon': None}
                },
            'staves': 
                {'end jab': 
                    {'uid': 'stave end jab', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': 'stave'},
                'parting jab': 
                    {'uid': 'stave parting jab', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': 'stave'},
                'parting swat': 
                    {'uid': 'stave parting swat', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': 'stave'},
                'simple strike': 
                    {'uid': 'stave simple strike', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': 'stave'},
                'swat': 
                    {'uid': 'stave swat', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': 'stave'},
                'parting smash':
                     {'uid': 'stave parting smash', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high', 'weapon': 'stave'},
                'pivot smash': 
                    {'uid': 'stave pivot smash', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': 'stave'},
                'side strike': 
                    {'uid': 'stave side strike', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': 'stave'},
                'snapstrike': 
                    {'uid': 'stave snapstrike', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high', 'weapon': 'stave'},
                'stepping spin': 
                    {'uid': 'stave stepping spin', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': 'stave'},
                'longarm strike': 
                    {'uid': 'stave longarm strike', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high', 'weapon': 'stave'},
                'pivoting longarm': 
                    {'uid': 'stave pivoting longarm', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': 'stave'},
                'spinstrike': 
                    {'uid': 'stave spinstrike', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high', 'weapon': 'stave'},
                'sweep strike': 
                    {'uid': 'stave sweep strike', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': ['low', 'high'], 'weapon': 'stave'},
                'triple bash': 
                    {'uid': 'stave triple bash', 'skill_type': 'offense', 'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high', 'weapon': 'stave'},
                'mid block': 
                    {'uid': 'stave mid block', 'skill_type': 'defense', 'damage_type': None, 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': 'stave'},
                'low block': 
                    {'uid': 'stave low block', 'skill_type': 'defense', 'damage_type': None, 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low', 'weapon': 'stave'},
                'overhead block': 
                    {'uid': 'stave overhead block', 'skill_type': 'defense', 'damage_type': None, 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high', 'weapon': 'stave'},
                'defensive sweep': 
                    {'uid': 'stave defensive sweep', 'skill_type': 'utility', 'damage_type': None, 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low', 'weapon': 'stave'},
                'feint': 
                    {'uid': 'stave feint', 'skill_type': 'utility', 'damage_type': None, 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low', 'weapon': 'stave'},
                'leg sweep': 
                    {'uid': 'stave leg sweep', 'skill_type': 'utility', 'damage_type': None, 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'low', 'weapon': 'stave'}
                },
            'holy':
                {'heal':
                    {'uid': 'stave swat', 'skill_type': 'utility', 'damage_type': 'heal', 'difficulty': 'average', 'hands': 0, 'attack_range': 'either', 'default_aim': 'mid', 'weapon': None}
                },
            'rat':
                {'bite':
                    {'uid': 'rat bite', 'skill_type': 'offense', 'damage_type': 'pierce', 'difficulty': 'easy', 'hands': 0, 'attack_range': 'melee', 'default_aim': 'high', 'weapon': 'bite'},
                'claw':
                    {'uid': 'rat claw', 'skill_type': 'offense', 'damage_type': 'slash', 'difficulty': 'easy', 'hands': 0, 'attack_range': 'melee', 'default_aim': 'mid', 'weapon': 'claw'}
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

def return_rank_score(rank, difficulty):
    if difficulty == 'easy':
        rs = easy_rs
    elif difficulty == 'average':
        rs = average_rs
    elif difficulty == 'difficult':
        rs = difficult_rs
    elif difficulty == 'impossible':
        rs = impossible_rs

    rs = rs[rank - 1]
    return rs

def return_defense_skills(char, skillset, rs_only=False, skills_only=False):
    high_rs, mid_rs, low_rs = 0, 0, 0
    high_skill, mid_skill, low_skill = '', '', ''
    rank = 0
    difficulty = ''
    defense_skill_list = []

    char_skillset_dic = char.attributes.get(skillset)
    skills = [*char_skillset_dic] # Create a list of the skill names.

    # Check each key in the dictionary against all viable skills.
    for i in skills:
        if skillsets[skillset].get(i):
            # Skill is in the main dictionary. Check if it's a defense skill.
            if skillsets[skillset][i]['skill_type'] == 'defense':
                defense_skill_list.append(i)

    # Sort each defensive skill by region defended.
    for i in defense_skill_list:
        rank = char_skillset_dic.get(i)
        difficulty = skillsets[skillset][i]['difficulty']
        if skillsets[skillset][i]['default_aim'] == 'high':
            high_rs = return_rank_score(rank, difficulty)
            high_skill = skillsets[skillset][i]['uid']
        elif skillsets[skillset][i]['default_aim'] == 'mid':
            mid_rs = return_rank_score(rank, difficulty)
            mid_skill = skillsets[skillset][i]['uid']
        elif skillsets[skillset][i]['default_aim'] == 'low':
            low_rs = return_rank_score(rank, difficulty)
            low_skill = skillsets[skillset][i]['uid']

    # Return the values       
    if rs_only == True:
        return high_rs, mid_rs, low_rs
    elif skills_only == True:
        return high_skill, mid_skill, low_skill
    else:
        return high_rs, mid_rs, low_rs, high_skill, mid_skill, low_skill

def defense_layer_calc(char, rs_only=False, skills_only=False):
    """
    Defensive rank score includes up to 3 layers of defense.
    The highest RS defensive manuever of each high, mid, and low will gain 100% of it's RS.
    The second highest RS will supply 50% and the third will only be worth 33%.
    Each layer can only consist of a single defensive manuever from each of the following categories:
        Weapon Blocks, Combat Manuever Dodges, and Shield Blocks.
        Weapons that require 2 hands can only ever gain 2 defensive layers. 
        Shields or offhand weapons are the only way to gain all 3 layers.

    For Example:
    Staves Mid Block with 100 rank score * 1 = 100
    CM Mid Dodge with 80 rank score * 0.5 = 40
    Total Mid Defensive rank score = 140

    Swords Mid Block with 100 rank score * 0.33 = 33
    CM Mid Dodge with 150 rank score * 0.5 = 75
    Shield Mid Block with 200 rank score * 1 = 200
    Total Mid Defensive rank score = 308

    Floats are used to determine the highest RS priority, but only rounded down integers are used to determine the total RS.

    TODO: Add a round down for the final RS.

    High, Mid, and Low always refer to the area 
    of the body that the attack targets and not the numerical value.
    """

    weap_high_skill, weap_mid_skill, weap_low_skill = None, None, None
    offhand_high_skill, offhand_mid_skill, offhand_low_skill = None, None, None
    dodge_high_skill, dodge_mid_skill, dodge_low_skill = None, None, None

    # Initialize rankscore values.
    weap_high_rs, weap_mid_rs, weap_low_rs = 0.0, 0.0, 0.0
    offhand_high_rs, offhand_mid_rs, offhand_low_rs = 0.0, 0.0, 0.0
    dodge_high_rs, dodge_mid_rs, dodge_low_rs = 0.0, 0.0, 0.0

    # Acquire the item(s) wielded.
    if char.attributes.get('wielding'):
        wielding  = char.attributes.get('wielding')
        l_wield = wielding.get('left')
        r_wield = wielding.get('right')
        b_wield = wielding.get('both')
    
        if b_wield:
            if b_wield.attributes.has('skillset'):
                item_skillset = b_wield.attributes.get('skillset')
                weap_high_rs, weap_mid_rs, weap_low_rs = return_defense_skills(char, item_skillset, rs_only=True)
                weap_high_skill, weap_mid_skill, weap_low_skill = return_defense_skills(char, item_skillset, skills_only=True)
        if r_wield:
            if r_wield.attributes.has('skillset'):
                item_skillset = r_wield.attributes.get('skillset')
                weap_high_rs, weap_mid_rs, weap_low_rs = return_defense_skills(char, item_skillset, rs_only=True)
                weap_high_skill, weap_mid_skill, weap_low_skill = return_defense_skills(char, item_skillset, skills_only=True)
        if l_wield:
            if l_wield.attributes.has('skillset'):
                item_skillset = l_wield.attributes.get('skillset')
                offhand_high_rs, offhand_mid_rs, offhand_low_rs = return_defense_skills(char, item_skillset, rs_only=True)
                offhand_high_skill, offhand_mid_skill, offhand_low_skill = return_defense_skills(char, item_skillset, skills_only=True)

    # Get all dodge rank scores
    if char.attributes.get('martial arts'):
        dodge_high_skill, dodge_mid_skill, dodge_low_skill = return_defense_skills(char, 'martial arts', skills_only=True)
        dodge_high_rs, dodge_mid_rs, dodge_low_rs = return_defense_skills(char, 'martial arts', rs_only=True)
    
    high_skills = [weap_high_skill, offhand_high_skill, dodge_high_skill]
    mid_skills = [weap_mid_skill, offhand_mid_skill, dodge_mid_skill]
    low_skills = [weap_low_skill, offhand_low_skill, dodge_low_skill]
    
    # High Layer
    h_rs = [weap_high_rs, offhand_high_rs, dodge_high_rs]
    h_rs.sort(reverse=True)
    h_layer1 = h_rs[0] * 1
    h_layer2 = h_rs[1] * 0.5
    h_layer3 = h_rs[2] * 0.33
    high_def_rs = (h_layer1 + h_layer2 + h_layer3)

    # Mid Layer
    m_rs = [weap_mid_rs, offhand_mid_rs, dodge_mid_rs]
    m_rs.sort(reverse=True)
    m_layer1 = m_rs[0] * 1
    m_layer2 = m_rs[1] * 0.5
    m_layer3 = m_rs[2] * 0.33
    mid_def_rs = (m_layer1 + m_layer2 + m_layer3)

    # Low Layer
    l_rs = [weap_low_rs, offhand_low_rs, dodge_low_rs]
    l_rs.sort(reverse=True)
    l_layer1 = l_rs[0] * 1
    l_layer2 = l_rs[1] * 0.5
    l_layer3 = l_rs[2] * 0.33
    low_def_rs = (l_layer1 + l_layer2 + l_layer3)

    if rs_only:
        return high_def_rs, mid_def_rs, low_def_rs
    elif skills_only:
        return high_skills, mid_skills, low_skills
    else:
        return high_skills, mid_skills, low_skills, high_def_rs, mid_def_rs, low_def_rs

def rs_stance(self, o_rs, d_rs, stance):
    '''
    o_rs = Offensive rank score
    d_rs = Defensive rank score

    Berserk - Attack 100% | Defense: 0%
    Aggressive - Attack 75% | Defense: 25%
    Normal - Attack 50% | Defense: 50%
    Wary - Attack 25% | Defense: 75%
    Defensive - Attack 0% | Defense: 100%
    '''
    if stance == 'berserk':
        o_rs = o_rs * 1
        d_rs = d_rs * 0
        return o_rs, d_rs
    if stance == 'aggressive':
        o_rs = o_rs * 0.75
        d_rs = d_rs * 0.25
        return o_rs, d_rs
    if stance == 'normal':
        o_rs = o_rs * 0.5
        d_rs = d_rs * 0.5
        return o_rs, d_rs
    if stance == 'wary':
        o_rs = o_rs * 0.25
        d_rs = d_rs * 0.75
        return o_rs, d_rs
    if stance == 'defensive':
        o_rs = o_rs * 0
        d_rs = d_rs * 1
        return o_rs, d_rs


def learn_skillset(char, skillset):
    # Check if the skillset is not already learned and if not, create it.
    if not char.attributes.has(skillset):
        generate_fresh_skillset(char, skillset)
        char.msg(f"You learn {skillset}.")
    else:
        char.msg(f"You already know {skillset}!")

def generate_fresh_skillset(char, skillset, starting_rank=1):
    # store lists of baseline skills for each skillset
    base_dic = {'base ranks': starting_rank, 'bonus ranks': 0, 'current ap': 0}
    staves = {'end jab': 1, 'parting jab': 1, 'parting swat': 1, 'simple strike': 1, 'swat': 1, 
                'parting smash': 1, 'pivot smash': 1, 'side strike': 1, 'snapstrike': 1, 'stepping spin': 1, 
                'longarm strike': 1, 'pivoting longarm': 1, 'spinstrike': 1, 'sweep strike': 1, 'triple bash': 1, 
                'mid block': 1, 'low block': 1, 'overhead block': 1, 'defensive sweep': 1, 'feint': 1, 'leg sweep': 1}
    holy = {'heal': 1}
    marts = {'dodge': 1, 'duck': 1, 'jump': 1}
    # setup all the fresh new skills and set them to 0 in a new skillset
    if skillset == 'staves':
        char.attributes.add(skillset, {**base_dic, **staves})
    elif skillset == 'holy':
        char.attributes.add(skillset, {**base_dic, **holy})
    elif skillset == 'martial arts':
        char.attributes.add(skillset, {**base_dic, **marts})
    

def grant_ap(char, skillset):
    if char.attributes.get(skillset):
        skillset_dic = char.attributes.get(skillset)
        base_ranks = skillset_dic.get('base ranks')
        current_ap = skillset_dic.get('current ap')
        desired_rank = base_ranks + 1
        ap_gain = generate_ap()
        total_ap = current_ap + ap_gain

        ap_req = ap_required(desired_rank)

        if total_ap >= ap_req: # Level up!
            ap_diff = total_ap - ap_req
            skillset_dic['current ap'] = ap_diff
            skillset_dic['base ranks'] = base_ranks + 1
            char.msg(f"You have reached the base rank of {skillset_dic['base ranks']} in {skillset}!")
        else:
            skillset_dic['current ap'] = total_ap
            char.msg(f"You have gained {ap_gain} AP toward your {skillset} skillset with {ap_req - total_ap} AP remaining to level.")

def return_skill_rank(char, skillset, skill):
    skill_rank = 0
    if char.attributes.has(skillset):
        skillset_dic = char.attributes.get(skillset)
        skillset_base_rank = skillset_dic.get('base ranks')
        skillset_bonus_rank = skillset_dic.get('bonus ranks')
        skillset_rank = skillset_base_rank + skillset_bonus_rank
        if skillset_dic.get(skill):
            skill_bonus_rank = skillset_dic.get(skill)
            skill_bonus_rank -= 1 # Must remove the base rank required for value parsing.
            skill_rank = skillset_rank + skill_bonus_rank
    return skill_rank

def generate_skill_list(char):
    """
    Desired Outcome

    =====[Skills]=====================================

    {skillset_name}
    -------------------------------
    Offense:
    {skill_name}            Rank: {rank}        Rank Score: {rank_score}

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

    offense_skill_base_rank_list = []
    defense_skill_base_rank_list = []
    utility_skill_base_rank_list = []

    offense_skill_bonus_rank_list = []
    defense_skill_bonus_rank_list = []
    utility_skill_bonus_rank_list = []
    
    offense_rank_score_list = []
    defense_rank_score_list = []
    utility_rank_score_list = []

    offense_skill_string_list = []
    defense_skill_string_list = []
    utility_skill_string_list = []

    skillset_string_list = []

    skillset_dic = None
    skill_base_rank = 0
    skill_bonus_rank = 0
    skill_rank = 0
    skill_rank_score = 0.0
    skill_difficulty = ''

    num = 0
    offense_skill_string = ""
    defense_skill_string = ""
    utility_skill_string = ""
    full_skillsets_string = ""

    header = "=====[|gSkills|n]====================================="
    footer = "=================================================="

  
    for i in VIABLE_SKILLSETS:
        # We reset the skill lists at the start of each new skillset iteration.
        offense_skill_string = ""
        defense_skill_string = ""
        utility_skill_string = ""

        offense_skill_list = []
        defense_skill_list = []
        utility_skill_list = []

        offense_rank_list = []
        defense_rank_list = []
        utility_rank_list = []

        offense_skill_base_rank_list = []
        defense_skill_base_rank_list = []
        utility_skill_base_rank_list = []

        offense_skill_bonus_rank_list = []
        defense_skill_bonus_rank_list = []
        utility_skill_bonus_rank_list = []

        offense_rank_score_list = []
        defense_rank_score_list = []
        utility_rank_score_list = []

        offense_skill_string_list = []
        defense_skill_string_list = []
        utility_skill_string_list = []

        if char.attributes.get(i): # If the skillset exists on the character.
            skillset_dic = char.attributes.get(i) # Store that skillset's dictionary.
            print(f"skillset_dic = {skillset_dic}")
            base_ranks = skillset_dic.get('base ranks')
            bonus_ranks = skillset_dic.get('bonus ranks')
            skill_base_rank = base_ranks + bonus_ranks
            current_ap = skillset_dic.get('current ap')
            next_rank_ap_req = ap_required(base_ranks + 1)
            ap_remaining = next_rank_ap_req - current_ap

            # Build skill lists
            for x in VIABLE_SKILLS:
                if skillset_dic.get(x): # If the skill exists on the character.
                    print(f"skill acquire = {skillset_dic.get(x)}")
                    skill_bonus_rank = skillset_dic.get(x) # Store that skill's bonus
                    skill_bonus_rank -= 1 # Must remove the base rank required to parse the key.
                    print(f"skill_bonus_rank = {skill_bonus_rank}")
                    skill_rank = return_skill_rank(char, i, x)
                    skill_difficulty = skillsets[i][x]['difficulty']
                    skill_rank_score = return_rank_score(skill_rank, skill_difficulty)

                    # Store the skill's name in a list, sorted by skill type.
                    if skillsets[i][x]['skill_type'] == 'offense':
                        offense_skill_list.append(x)
                        offense_skill_base_rank_list.append(skill_base_rank)
                        offense_skill_bonus_rank_list.append(skill_bonus_rank)
                        offense_rank_list.append(skill_rank)
                        offense_rank_score_list.append(skill_rank_score)
                    elif skillsets[i][x]['skill_type'] == 'defense':
                        defense_skill_list.append(x)
                        defense_skill_base_rank_list.append(skill_base_rank)
                        defense_skill_bonus_rank_list.append(skill_bonus_rank)
                        defense_rank_list.append(skill_rank)
                        defense_rank_score_list.append(skill_rank_score)
                    elif skillsets[i][x]['skill_type'] == 'utility':
                        utility_skill_list.append(x)
                        utility_skill_base_rank_list.append(skill_base_rank)
                        utility_skill_bonus_rank_list.append(skill_bonus_rank)
                        utility_rank_list.append(skill_rank)
                        utility_rank_score_list.append(skill_rank_score)

            # Build this skillset's string.
            skillset_title = (f"\n\n|g{cap(i)}|n - Base Ranks: |g{base_ranks}|n    Bonus Ranks: |g{bonus_ranks}|n\n"
                            f"Current ap: {current_ap}    Rank {base_ranks + 1} AP Requirement: {next_rank_ap_req}    Required AP Remaining: |c{ap_remaining}|n\n"
                        "--------------------------------------------------")
            num = 0
            for v in offense_skill_list:
                offense_skill_string_list.append(f"|G{cap(v)}|n    Base Rank: |G{offense_skill_base_rank_list[num]}|n    Bonus Ranks: |G{offense_skill_bonus_rank_list[num]}|n    Rank: |G{offense_rank_list[num]}|n    Rank Score: |G{offense_rank_score_list[num]}|n\n")
                num += 1
            if len(offense_skill_string_list) > 0:
                offense_skill_string = f"\nOffense:\n{''.join(offense_skill_string_list)}"

            num = 0
            for v in defense_skill_list:
                defense_skill_string_list.append(f"|G{cap(v)}|n    Base Rank: |G{defense_skill_base_rank_list[num]}|n    Bonus Ranks: |G{defense_skill_bonus_rank_list[num]}|n    Rank: |G{defense_rank_list[num]}|n    Rank Score: |G{defense_rank_score_list[num]}|n\n")
                num += 1
            if len(defense_skill_string_list) > 0:
                defense_skill_string = f"\nDefense:\n{''.join(defense_skill_string_list)}"

            num = 0
            for v in utility_skill_list:
                utility_skill_string_list.append(f"|G{cap(v)}|n    Base Rank: |G{utility_skill_base_rank_list[num]}|n    Bonus Ranks: |G{utility_skill_bonus_rank_list[num]}|n    Rank: |G{utility_rank_list[num]}|n    Rank Score: |G{utility_rank_score_list[num]}|n\n")
                num += 1
            if len(utility_skill_string_list) > 0:
                utility_skill_string = f"\nUtility:\n{''.join(utility_skill_string_list)}"
            
            skillset_string_list.append(f"{skillset_title}{offense_skill_string}{defense_skill_string}{utility_skill_string}")

    # Now we compile the final list.
    full_skillsets_string = ''.join(skillset_string_list)

    # Current total defensive rank scores.
    high_def_rs, mid_def_rs, low_def_rs = defense_layer_calc(char, rs_only=True)
    def_rs = f"\n\nCurrent total defensive RS - High: {high_def_rs}    Mid: {mid_def_rs}    Low: {low_def_rs}\n"

    result = f"{header}{full_skillsets_string}{def_rs}\n{footer}"
    return result