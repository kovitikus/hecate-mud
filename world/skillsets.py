class rank_bonus():
    def rb_calc(self):
        '''
        Order of rank bonus calculation.
            Skill Level
            Stance
        '''
        pass
    
    def skill_level(self, rank, difficulty):
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
        #Temp Values
        rb = 0
        rank = 100

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
            #15% RB loss per difficulty. At rank 100: Easy(100%) 115 RB, Average(85%) 97.75 RB, Difficult(70%) 80.5 RB, Impossible(55%) 63.25 RB.
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

class training():
    def gain_sp(self, skill):
        pass

    def learn_skill(self, char, skillset, skill):
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
        skill_data = []
        skill_data = skillsets.skillset.skill()
        gsp = char.attributes.get('gsp')
        
        # Set the per rank SP cost of the skill.
        sp_cost = 0
        if skill_data[1] == 'easy':
            sp_cost = 5
        elif skill_data[1] == 'average':
            sp_cost = 7
        elif skill_data[1] == 'difficult':
            sp_cost = 9
        elif skill_data[1] == 'impossible':
            sp_cost = 11
        
        # Check if the skillset is not already learned and if not, create it.
        if not char.attributes.get(skillset):
            #Check for general skill points required to learn.
            if not gsp >= sp_cost:
                char.msg('You do not have enough general skill points to learn this skillset.')
                return
            if skillset == 'staves':
                char.db.staves = {'total_sp': sp_cost, 'total_ranks': 0}

        # Check for stave skills.
        if skillset == 'staves':
            if not char.db.staves['total_sp'] >= sp_cost:
                char.msg('You do not have enough skill points to learn this skill.')
                return
            if not char.db.staves[skill]:
                char.db.staves[skill] = {'rank': 0, 'rb': 0}
            char.db.staves[skill]['rank'] += 1
            char.db.staves['total_sp'] -= sp_cost
            rank = char.db.staves[skill]['rank']
            rb = skillsets.rank_bonus.skill_level(rank, skill_data[1])
            char.db.staves[skill]['rb'] = rb
            char.msg(f'Created {skillset} and added {skill} of rank {char.db.staves[skill][rank]} with rank bonus of {char.db.staves[skill]["rb"]}.')


class staves():
    def leg_sweep(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'low'
        return damge_type, difficulty, hands, attk_range, default_aim

    def feint(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'
        return damge_type, difficulty, hands, attk_range, default_aim

    def end_jab(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'
        return damge_type, difficulty, hands, attk_range, default_aim

    def swat(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'
        return damge_type, difficulty, hands, attk_range, default_aim

    def simple_strike(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'
        return damge_type, difficulty, hands, attk_range, default_aim

    def side_strike(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'
        return damge_type, difficulty, hands, attk_range, default_aim

    def pivot_smash(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'
        return damge_type, difficulty, hands, attk_range, default_aim

    def longarm_strike(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'
        return damge_type, difficulty, hands, attk_range, default_aim

    def simple_block(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = ('mid', 'low')
        return damge_type, difficulty, hands, attk_range, default_aim

    def cross_block(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = ('mid', 'low')
        return damge_type, difficulty, hands, attk_range, default_aim

    def overhead_block(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'
        return damge_type, difficulty, hands, attk_range, default_aim

    def parting_jab(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'
        return damge_type, difficulty, hands, attk_range, default_aim

    def parting_swat(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'
        return damge_type, difficulty, hands, attk_range, default_aim

    def parting_smash(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'
        return damge_type, difficulty, hands, attk_range, default_aim

    def defensive_sweep(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'low'
        return damge_type, difficulty, hands, attk_range, default_aim

    def stepping_spin(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'
        return damge_type, difficulty, hands, attk_range, default_aim

    def snapstrike(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'
        return damge_type, difficulty, hands, attk_range, default_aim

    def sweep_strike(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = ('low', 'high')
        return damge_type, difficulty, hands, attk_range, default_aim

    def spinstrike(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'
        return damge_type, difficulty, hands, attk_range, default_aim

    def tbash(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'
        return damge_type, difficulty, hands, attk_range, default_aim

    def whirling_block(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'
        return damge_type, difficulty, hands, attk_range, default_aim

    def pivoting_longarm(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'
        return damge_type, difficulty, hands, attk_range, default_aim