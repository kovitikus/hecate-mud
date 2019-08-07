class rank_bonus():
    def rb_calc(self):
        '''
        Order of rank bonus calculation.
            Skill Level
            Skill Difficulty (Additive)

        '''
        pass
    
def skill_level(self, rank):
    '''
    RANK += RANK BONUS
    --------------------------
    1 to 9 += 3
    10 to 19 += 2
    20 to 29 += 2
    30 to 39 += 1
    40 to 49 += 1
    50 to 59 += 0.5
    60 to 69 += 0.5
    70 to 79 += 0.5
    80 to 89 += 0.5
    90 to 100 += 0.5
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
        r = rank if rank < 9 else 9
        rb += (3 * r)
        if rank >= 10:
            r = rank - 9 if rank < 19 else 10
            rb += (2 * r)
            if rank >= 20:
                r = rank - 19 if rank < 29 else 10
                rb += (2 * r)
                if rank >= 30:
                    r = rank - 29 if rank < 39 else 10
                    rb += (1 * r)
                    if rank >= 40:
                        r = rank - 39 if rank < 49 else 10
                        rb += (1 * r)
                        if rank >= 50:
                            r = rank - 49 if rank < 59 else 10
                            rb += (0.5 * r)
                            if rank >= 60:
                                r = rank - 59 if rank < 69 else 10
                                rb += (0.5 * r)
                                if rank >= 70:
                                    r = rank - 69 if rank < 79 else 10
                                    rb += (0.5 * r)
                                    if rank >= 80:
                                        r = rank - 79 if rank < 89 else 10
                                        rb += (0.5 * r)
                                        if rank >= 90:
                                            r = rank - 89 if rank < 100 else 11
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
        return rb # Return if any rank.
    return None # Return if no rank.


    def rb_stance(self, o_rb, d_rb):
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

class Staves():
    def leg_sweep(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'low'

    def feint(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'

    def end_jab(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'

    def swat(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'

    def simple_strike(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'

    def side_strike(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'

    def pivot_smash(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'

    def longarm_strike(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'

    def simple_block(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = ('mid', 'low')

    def cross_block(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = ('mid', 'low')

    def overhead_block(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'

    def parting_jab(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'

    def parting_swat(self):
        damge_type = 'bruise'
        difficulty = 'easy'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'

    def parting_smash(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'

    def defensive_sweep(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'low'

    def stepping_spin(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'

    def snapstrike(self):
        damge_type = 'bruise'
        difficulty = 'average'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'

    def sweep_strike(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = ('low', 'high')

    def spinstrike(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'

    def tbash(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'

    def whirling_block(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = 'high'

    def pivoting_longarm(self):
        damge_type = 'bruise'
        difficulty = 'difficult'
        hands = 2
        attk_range = 'either'
        default_aim = 'mid'