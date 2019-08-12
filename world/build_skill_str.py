from world import generic_str

article = generic_str.article
pronoun = generic_str.pronoun

def create_attack_desc(attacker, target, damage_type, damage_tier, body_part):
    # Temp Values
    damage_type = ''
    damage_tier = ''
    body_part = 'head'
    outcome = ''
    weapon = ''
    
    

    wound_tier = {'slash': ['shallow cut', 'cut', 'deep cut', 'severe cut', 'devastating cut'],
        'pierce': ['faint wound', 'puncture', 'deep puncture', 'severe puncture', 'gaping wound'],
        'bruise': ['small bruise', 'bruise', 'ugly bruise', 'major bruise', 'fracture']}
    attack_wound = wound_tier[damage_type][damage_tier]

    # Attacker and target pronouns. Possessive (its, his, her), Singular Subject (it, he, she), Singular Object (it, him, her)
    a_poss, a_sin_sub, a_sin_obj = pronoun(attacker)
    t_poss, t_sin_sub, t_sin_obj = pronoun(target)

    a_name = attacker.key
    t_name = target.key

    # Weapon's article. 'a' or 'an'
    art_weap = article(weapon)

    a_msg = str.capitalize(f"{t_sin_sub} suffers {article(attack_wound)} {attack_wound} to {t_poss} {body_part}.")
    t_msg = f"you suffer {article(attack_wound)} {attack_wound} to your {body_part}."

    staves = {'leg sweep': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'feint': {'attack_desc': {'self': f"You sweep your {weapon} at {target}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'end jab': {'attack_desc': {'self': f"You sweep your {weapon} at {target}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'swat': {'attack_desc': {'self': f"Using the center of a {weapon} as a fulcrum, you swat at {t_name} with one end of the weapon,",
                                            'other': f"Using the center of a {weapon} as a fulcrum, {attacker} swats at {t_name} with one end of the weapon, {outcome}."}},
            'simple strike': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'side strike': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'pivot smash': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'longarm strike': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'simple block': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'cross block': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'overhead block': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'parting jab': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'parting swat': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'parting smash': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'defensive sweep': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'stepping spin': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'snapstrike': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'sweep strike': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'spinstrike': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'tbash': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'whirling block': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}},
            'pivoting longarm': {'attack_desc': {'self': f"You sweep your {weapon} at {t_name}\'s legs, {outcome}.",
                                            'other': f"{a_name} sweeps {article(weapon)} {weapon} at {t_name}\'s legs, {outcome}."}}}

    return attacker_desc, target_desc