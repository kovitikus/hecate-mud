
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
                    {'damage_type': 'weapon_block', 'difficulty': 'easy', 'hands': 2, 'attack_range': 'either', 'default_aim': ('mid', 'low')},
                'cross block': 
                    {'damage_type': 'weapon_block', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': ('mid', 'low')},
                'overhead block': 
                    {'damage_type': 'weapon_block', 'difficulty': 'average', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
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
                    {'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': ('low', 'high')},
                'spinstrike': 
                    {'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'tbash': 
                    {'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'whirling block': 
                    {'damage_type': 'weapon_block', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'high'},
                'pivoting longarm': 
                    {'damage_type': 'bruise', 'difficulty': 'difficult', 'hands': 2, 'attack_range': 'either', 'default_aim': 'mid'}
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
    d_skillset[skill]['rb'] = rb[rank - 1]
    d_skillset['total_ranks'] += 1
    char.msg(f"You have spent {sp_cost} SP to learn rank {rank} of {skillset} {skill}, earning the rank bonus of {d_skillset[skill]['rb']}.")