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