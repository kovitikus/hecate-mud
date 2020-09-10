import random
from world import generic_str
from world import skillsets

article = generic_str.article
pronoun = generic_str.pronoun
prop_name = generic_str.proper_name
                    
def create_attack_desc(attacker, target, skillset, skill, weapon, damage_type, damage_tier, body_part, hit, aim):
    cap = str.capitalize

    wound_tier = {'slash': ['shallow cut', 'cut', 'deep cut', 'severe cut', 'devastating cut'],
                'pierce': ['faint wound', 'puncture', 'deep puncture', 'severe puncture', 'gaping wound'],
                'bruise': ['small bruise', 'bruise', 'ugly bruise', 'major bruise', 'fracture']}
    attack_wound = wound_tier[damage_type][damage_tier]

    # Attacker and target pronouns. Possessive (its, his, her), Singular Subject (it, he, she), Singular Object (it, him, her)
    a_poss, a_sin_sub, a_sin_obj = pronoun(attacker)
    t_poss, t_sin_sub, t_sin_obj = pronoun(target)
    
    # TODO: Creatures and other non-proper named entities shouldn't be capitalized except at the beginning of a sentence.
    a_name = prop_name(attacker)
    t_name = prop_name(target)
    c_a_name = cap(attacker.key)
    c_t_name = cap(target.key)

    # Weapon's article. 'a' or 'an'
    if attacker.attributes.has('wielding'):
        wielded = attacker.attributes.get('wielding')
        if wielded.get('both'):
            both_weap = wielded.get('both')
            art_weap = article(both_weap.name)
        elif wielded.get('right'):
            right_weap = wielded.get('right')
            art_weap = article(right_weap.name)
        else:
            art_weap = article(weapon)

    if hit:
        a_outcome = f"{cap(t_sin_sub)} suffers {article(attack_wound)} {attack_wound} to {t_poss} {body_part}."
        t_outcome = f"You suffer {article(attack_wound)} {attack_wound} to your {body_part}."
        o_outcome = f"{c_t_name} suffers {article(attack_wound)} {attack_wound} to {t_poss} {body_part}."
    else:
        a_outcome, t_outcome, o_outcome = create_defense_desc(target, aim, c_a_name, art_weap, weapon, t_name)

    skillsets = {'staves': 
                    {'leg sweep': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'feint': 
                        {'attacker': f"You sweep your {weapon} at {target}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'end jab': 
                        {'attacker': f"You sweep your {weapon} at {target}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'swat': 
                        {'attacker': f"Using the center of {art_weap} {weapon} as a fulcrum, you swat at {t_name} with one end of the weapon! {a_outcome}",
                        'target': f"Using the center of {art_weap} {weapon} as a fulcrum, {attacker} swats at you with one end of the weapon! {t_outcome}",
                        'others': f"Using the center of {art_weap} {weapon} as a fulcrum, {attacker} swats at {t_name} with one end of the weapon! {o_outcome}"},
                    'simple strike': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'side strike': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'pivot smash': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'longarm strike': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'parting jab': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'parting swat': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'parting smash': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'defensive sweep': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'stepping spin': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'snapstrike': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'sweep strike': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'spinstrike': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},         
                    'tbash': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'whirling block': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"},
                    'pivoting longarm': 
                        {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                        'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}
                    },
                                            
                'rat': 
                    {'claw': 
                        {'attacker': f"You claw at {t_name} with your front paws! {a_outcome}",
                        'target': f"{c_a_name} claws at you with {a_poss} front paws! {t_outcome}",
                        'others': f"{c_a_name} claws at {t_name} with {a_poss} front paws! {o_outcome}"},
                    'bite': 
                        {'attacker': f"You bite at {t_name} with your teeth! {a_outcome}",
                        'target': f"{c_a_name} bites at you with {a_poss} teeth! {t_outcome}",
                        'others': f"{c_a_name} bites at {t_name} with {a_poss} teeth! {o_outcome}"}
                    }
                }

    attacker_desc = skillsets[skillset][skill]['attacker']
    target_desc = skillsets[skillset][skill]['target']
    others_desc = skillsets[skillset][skill]['others']

    return attacker_desc, target_desc, others_desc

def create_defense_desc(target, aim, c_a_name, art_weap, weapon, t_name):
    high_skills, mid_skills, low_skills = skillsets.defense_layer_calc(target, skills_only=True)
    def_skills = []
    miss_chance = 20
    targ_weap = None
    targ_offhand = None
    art_targ_weap = None
    art_targ_offhand = None

    #Get target wielded weapon.
    if target.attributes.get('wielding'):
        targ_wield = target.attributes.get('wielding')
        if targ_wield.get('both'):
            targ_weap = targ_wield['both']
            art_targ_weap = article(targ_weap.name)
        if targ_wield.get('right'):
            targ_weap = targ_wield['right']
            art_targ_weap = article(targ_weap.name)
        if targ_wield.get('left'):
            targ_offhand = targ_wield['left']
            art_targ_offhand = article(targ_offhand.name)


    if aim == 'high':
        skills = high_skills
    elif aim == 'mid':
        skills = mid_skills
    elif aim == 'low':
        skills = low_skills

    layer_count = 0
    for i in skills:
        if i != None:
            layer_count += 1
            def_skills.append(i)
    
    roll = random.randint(0, 100)

    if roll > miss_chance and layer_count > 0:
        outcome = random.choice(def_skills)
    else:
        outcome = 'miss'

    defense_skills = {'miss':
                        {'attacker': "You miss!",
                        'target': f"{c_a_name} misses!",
                        'others': f"{c_a_name} misses!"},
                    'stave mid block':
                        {'attacker': f"{t_name} blocks your {weapon} with {art_targ_weap} {targ_weap}!",
                        'target': f"You block {c_a_name}\'s {weapon} with your {targ_weap}!",
                        'others': f"{t_name} blocks {c_a_name}\'s {weapon} with {art_targ_weap} {targ_weap}!"},
                    'stave low block':
                        {'attacker': f"{t_name} swings the butt of their {targ_weap} low and blocks your {weapon}!",
                        'target': f"You swing the butt of your {targ_weap} low and block {c_a_name}\'s {weapon}!",
                        'others': f"{t_name} swings the butt of their {targ_weap} low and blocks {c_a_name}\'s {weapon}!"},
                    'stave overhead block':
                        {'attacker': f"{t_name} raises their {targ_weap} high and blocks your {weapon}!",
                        'target': f"You raise your {targ_weap} high and block {c_a_name}\'s {weapon}!",
                        'others': f"{t_name} raises their {targ_weap} and blocks {c_a_name}\'s {weapon}!"},
                    'marts dodge':
                        {'attacker': f"{t_name} dodges your {weapon}!",
                        'target': f"You dodge {c_a_name}\'s {weapon}!",
                        'others': f"{t_name} dodges {c_a_name}\'s {weapon}!"},
                    'marts duck':
                        {'attacker': f"{t_name} squats low and ducks right under your {weapon}!",
                        'target': f"You squat low and duck right under {c_a_name}\'s {weapon}!",
                        'others': f"{t_name} squats low and ducks right under {c_a_name}\'s {weapon}!"},
                    'marts jump':
                        {'attacker': f"{t_name} jumps over your {weapon} and you fail to connect!",
                        'target': f"You jump over {c_a_name}\'s {weapon} and {c_a_name} fails to connect!",
                        'others': f"{t_name} jumps over {c_a_name}\'s {weapon} and {c_a_name} fails to connect!"}
                    }

    a_outcome = defense_skills[outcome]['attacker']
    t_outcome = defense_skills[outcome]['target']
    o_outcome = defense_skills[outcome]['others']

    return a_outcome, t_outcome, o_outcome

