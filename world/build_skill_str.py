from world import generic_str

article = generic_str.article
pronoun = generic_str.pronoun
prop_name = generic_str.proper_name

def create_attack_desc(attacker, target, skillset, skill, damage_type, damage_tier, body_part, hit):
    cap = str.capitalize
    # Temp Values
    weapon = 'quarterstave'

    wound_tier = {'slash': ['shallow cut', 'cut', 'deep cut', 'severe cut', 'devastating cut'],
        'pierce': ['faint wound', 'puncture', 'deep puncture', 'severe puncture', 'gaping wound'],
        'bruise': ['small bruise', 'bruise', 'ugly bruise', 'major bruise', 'fracture']}
    attack_wound = wound_tier[damage_type][damage_tier]

    # Attacker and target pronouns. Possessive (its, his, her), Singular Subject (it, he, she), Singular Object (it, him, her)
    a_poss, a_sin_sub, a_sin_obj = pronoun(attacker)
    t_poss, t_sin_sub, t_sin_obj = pronoun(target)

    a_name = prop_name(attacker)
    t_name = prop_name(target)
    c_a_name = cap(attacker.key)
    c_t_name = cap(target.key)

    # Weapon's article. 'a' or 'an'
    art_weap = article(weapon)
    if hit:
        a_outcome = f"{cap(t_sin_sub)} suffers {article(attack_wound)} {attack_wound} to {t_poss} {body_part}."
        t_outcome = f"You suffer {article(attack_wound)} {attack_wound} to your {body_part}."
        o_outcome = f"{c_t_name} suffers {article(attack_wound)} {attack_wound} to {t_poss} {body_part}."
    else:
        a_outcome = "You miss!"
        t_outcome = f"{c_a_name} misses!"
        o_outcome = f"{c_a_name} misses!"

    skillsets = {'staves': {'leg sweep': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'feint': {'attack_desc': {'attacker': f"You sweep your {weapon} at {target}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'end jab': {'attack_desc': {'attacker': f"You sweep your {weapon} at {target}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'swat': {'attack_desc': {'attacker': f"Using the center of {art_weap} {weapon} as a fulcrum, you swat at {t_name} with one end of the weapon! {a_outcome}",
                                            'target': f"Using the center of {art_weap} {weapon} as a fulcrum, {attacker} swats at you with one end of the weapon! {t_outcome}",
                                            'others': f"Using the center of {art_weap} {weapon} as a fulcrum, {attacker} swats at {t_name} with one end of the weapon! {o_outcome}"}},

            'simple strike': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'side strike': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'pivot smash': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'longarm strike': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'simple block': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'cross block': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'overhead block': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'parting jab': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'parting swat': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'parting smash': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'defensive sweep': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'stepping spin': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'snapstrike': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'sweep strike': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'spinstrike': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'tbash': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'whirling block': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}},

            'pivoting longarm': {'attack_desc': {'attacker': f"You sweep your {weapon} at {t_name}\'s legs, {a_outcome}",
                                            'others': f"{c_a_name} sweeps {art_weap} {weapon} at {t_name}\'s legs, {o_outcome}"}}},
                                            
            'rat': {'claw': {'attack_desc': {'attacker': f"You claw at {t_name} with your front paws! {a_outcome}",
                                                'target': f"{c_a_name} claws at you with {a_poss} front paws! {t_outcome}",
                                                'others': f"{c_a_name} claws at {t_name} with {a_poss} front paws! {o_outcome}"}}}}

    attacker_desc = skillsets[skillset][skill]['attack_desc']['attacker']
    target_desc = skillsets[skillset][skill]['attack_desc']['target']
    others_desc = skillsets[skillset][skill]['attack_desc']['others']

    return attacker_desc, target_desc, others_desc