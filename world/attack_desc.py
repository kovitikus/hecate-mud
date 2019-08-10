# target = None
# determiner = None
# attack_wound = None
# body_part = None

# attack_desc = {'attacker': f"{target} suffers {determiner} {attack_wound} to their {body_part}.", 'target': f"You suffer {determiner} {attack_wound} to your {body_part}."}

wound_tier = {'slash': ['shallow cut', 'cut', 'deep cut', 'severe cut', 'devastating cut'],
                'pierce': ['faint wound', 'puncture', 'deep puncture', 'severe puncture', 'gaping wound'],
                'bruise': ['small bruise', 'bruise', 'ugly bruise', 'major bruise', 'fracture']}


def create_attack_desc(attacker, target, damage_type, damage_tier, body_part):
    attack_wound = wound_tier[damage_type][damage_tier]
    determiner = 'an' if attack_wound[0] in ['a', 'e', 'i', 'o', 'u'] else 'a'

    if attacker.db.figure['gender'] == 'male':
        a_gender = 'his'
    elif attacker.db.figure['gender'] == 'female':
        a_gender = 'his'
    else:
        a_gender = 'its'

    if target.db.figure['gender'] == 'male':
        t_gender = 'his'
    elif target.db.figure['gender'] == 'female':
        t_gender = 'his'
    else:
        t_gender = 'its'
    

    attacker_desc = f"{target} suffers {determiner} {attack_wound} to {t_gender} {body_part}."
    target_desc = f"You suffer {determiner} {attack_wound} to your {body_part}."
    
    return attacker_desc, target_desc
