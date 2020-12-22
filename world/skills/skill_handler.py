from world.skills import skillsets

class SkillHandler():
    def __init__(self, owner):
        self.owner = owner
        self.generate_skillset_dics()

    def generate_skillset_dics(self):
        owner = self.owner
        skillset_dics = {}

        for i in skillsets.VIABLE_SKILLSETS:
            if owner.attributes.has(i):
                skillset_dic = dict(owner.attributes.get(i))
                skillset_dics[i] = skillset_dic
        self.skillset_dics = skillset_dics

    def generate_ap(self):
        ap_granted = 1
        # Here is where modifiers will kick in, such as rolling for the chance at extra AP.
        return ap_granted
    
    def ap_required(self, desired_rank):
        ap_per_rank = 100
        count = 0
        for _ in range(2, desired_rank+1):
            count += 1
            if count == 20:
                ap_per_rank += 10
                count = 0
        return ap_per_rank

    def return_rank_score(self, rank, difficulty):
        if difficulty == 'easy':
            rs = skillsets.easy_rs
        elif difficulty == 'average':
            rs = skillsets.average_rs
        elif difficulty == 'difficult':
            rs = skillsets.difficult_rs
        elif difficulty == 'impossible':
            rs = skillsets.impossible_rs

        rs = rs[rank - 1]
        return rs

    def return_defense_skills(self, skillset, rs_only=False, skills_only=False):
        high_rs, mid_rs, low_rs = 0, 0, 0
        high_skill, mid_skill, low_skill = '', '', ''
        rank = 0
        difficulty = ''
        defense_skill_list = []

        skills = [*self.skillset_dics[skillset]] # Create a list of the skill names.

        # Check each key in the dictionary against all viable skills.
        for i in skills:
            if i in skillsets.skillsets[skillset]:
                # Skill is in the main dictionary. Check if it's a defense skill.
                if skillsets.skillsets[skillset][i]['skill_type'] == 'defense':
                    defense_skill_list.append(i)

        # Sort each defensive skill by region defended.
        for i in defense_skill_list:
            rank = self.return_skill_rank(skillset, i)
            difficulty = skillsets.skillsets[skillset][i]['difficulty']
            if skillsets.skillsets[skillset][i]['default_aim'] == 'high':
                high_rs = self.return_rank_score(rank, difficulty)
                high_skill = skillsets.skillsets[skillset][i]['uid']
            elif skillsets.skillsets[skillset][i]['default_aim'] == 'mid':
                mid_rs = self.return_rank_score(rank, difficulty)
                mid_skill = skillsets.skillsets[skillset][i]['uid']
            elif skillsets.skillsets[skillset][i]['default_aim'] == 'low':
                low_rs = self.return_rank_score(rank, difficulty)
                low_skill = skillsets.skillsets[skillset][i]['uid']

        # Return the values       
        if rs_only == True:
            return high_rs, mid_rs, low_rs
        elif skills_only == True:
            return high_skill, mid_skill, low_skill
        else:
            return high_rs, mid_rs, low_rs, high_skill, mid_skill, low_skill

    def defense_layer_calc(self, rs_only=False, skills_only=False):
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
        owner = self.owner

        weap_high_skill, weap_mid_skill, weap_low_skill = None, None, None
        offhand_high_skill, offhand_mid_skill, offhand_low_skill = None, None, None
        dodge_high_skill, dodge_mid_skill, dodge_low_skill = None, None, None

        # Initialize rankscore values.
        weap_high_rs, weap_mid_rs, weap_low_rs = 0.0, 0.0, 0.0
        offhand_high_rs, offhand_mid_rs, offhand_low_rs = 0.0, 0.0, 0.0
        dodge_high_rs, dodge_mid_rs, dodge_low_rs = 0.0, 0.0, 0.0

        # Acquire the item(s) wielded.
        if owner.attributes.has('wielding'):
            wielding  = owner.attributes.get('wielding')
            main_wield = wielding.get('main')
            off_wield = wielding.get('off')
            b_wield = wielding.get('both')
        
            if b_wield:
                if b_wield.attributes.has('skillset'):
                    item_skillset = b_wield.attributes.get('skillset')
                    weap_high_rs, weap_mid_rs, weap_low_rs = self.return_defense_skills(item_skillset, rs_only=True)
                    weap_high_skill, weap_mid_skill, weap_low_skill = self.return_defense_skills(item_skillset, skills_only=True)
            if main_wield:
                if main_wield.attributes.has('skillset'):
                    item_skillset = main_wield.attributes.get('skillset')
                    weap_high_rs, weap_mid_rs, weap_low_rs = self.return_defense_skills(item_skillset, rs_only=True)
                    weap_high_skill, weap_mid_skill, weap_low_skill = self.return_defense_skills(item_skillset, skills_only=True)
            if off_wield:
                if off_wield.attributes.has('skillset'):
                    item_skillset = off_wield.attributes.get('skillset')
                    offhand_high_rs, offhand_mid_rs, offhand_low_rs = self.return_defense_skills(item_skillset, rs_only=True)
                    offhand_high_skill, offhand_mid_skill, offhand_low_skill = self.return_defense_skills(item_skillset, skills_only=True)

        # Get all dodge rank scores
        if owner.attributes.has('martial arts'):
            dodge_high_skill, dodge_mid_skill, dodge_low_skill = self.return_defense_skills('martial arts', skills_only=True)
            dodge_high_rs, dodge_mid_rs, dodge_low_rs = self.return_defense_skills('martial arts', rs_only=True)
        
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

    def return_damage_type(self, skillset, skill):
        if skillset in skillsets.VIABLE_SKILLSETS:
            if skill in skillsets.skillsets[skillset]:
                damage_type = skillsets.skillsets[skillset][skill]['damage_type']
                return damage_type

    def return_default_aim(self, skillset, skill):
        if skillset in skillsets.VIABLE_SKILLSETS:
            if skill in skillsets.skillsets[skillset]:
                default_aim = skillsets.skillsets[skillset][skill]['default_aim']
                return default_aim

    def learn_skillset(self, skillset):
        owner = self.owner

        # Check if the skillset is not already learned and if not, create it.
        if skillset not in self.skillset_dics:
            self.generate_fresh_skillset(skillset)
            owner.msg(f"You learn {skillset}.")
        else:
            owner.msg(f"You already know {skillset}!")

    def generate_fresh_skillset(self, skillset, starting_rank=1):
        owner = self.owner

        # Store dictionaries of baseline skills for each skillset.
        base_dic = {'base ranks': starting_rank, 'bonus ranks': 0, 'current ap': 0}
        staves = {'end jab': 0, 'parting jab': 0, 'parting swat': 0, 'simple strike': 0, 'swat': 0, 
                    'parting smash': 0, 'pivot smash': 0, 'side strike': 0, 'snapstrike': 0, 'stepping spin': 0, 
                    'longarm strike': 0, 'pivoting longarm': 0, 'spinstrike': 0, 'sweep strike': 0, 'triple bash': 0, 
                    'mid block': 0, 'low block': 0, 'overhead block': 0, 'defensive sweep': 0, 'feint': 0, 'leg sweep': 0}
        holy = {'heal': 0}
        marts = {'dodge': 0, 'duck': 0, 'jump': 0}
        rat = {'claw': 0, 'bite': 0}

        # setup all the fresh new skills and set them to 0 in a new skillset
        if skillset == 'staves':
            owner.attributes.add(skillset, {**base_dic, **staves})
            self.skillset_dics[skillset] = {**base_dic, **staves}
        elif skillset == 'holy':
            owner.attributes.add(skillset, {**base_dic, **holy})
            self.skillset_dics[skillset] = {**base_dic, **holy}
        elif skillset == 'martial arts':
            owner.attributes.add(skillset, {**base_dic, **marts})
            self.skillset_dics[skillset] = {**base_dic, **marts}
        elif skillset == 'rat':
            owner.attributes.add(skillset, {**base_dic, **rat})
            self.skillset_dics[skillset] = {**base_dic, **rat}

    def grant_action_points(self, skillset):
        owner = self.owner

        if skillset in self.skillset_dics:
            owner_skillset_saverdic = owner.attributes.get(skillset)

            base_ranks = self.skillset_dics[skillset]['base ranks']
            current_ap = self.skillset_dics[skillset]['current ap']

            desired_rank = base_ranks + 1
            ap_gain = self.generate_ap()
            total_ap = current_ap + ap_gain

            ap_req = self.ap_required(desired_rank)

            if total_ap >= ap_req: # Level up!
                ap_diff = total_ap - ap_req

                owner_skillset_saverdic['current ap'] = ap_diff
                self.skillset_dics[skillset]['current ap'] = ap_diff

                owner_skillset_saverdic['base ranks'] = base_ranks + 1
                self.skillset_dics[skillset]['base ranks'] = base_ranks + 1

                owner.msg(f"You have reached the base rank of {self.skillset_dics[skillset]['base ranks']} in {skillset}!")
            else:
                owner_skillset_saverdic['current ap'] = total_ap
                self.skillset_dics[skillset]['current ap'] = total_ap

                owner.msg(f"You have gained {ap_gain} AP toward your {skillset} skillset with {ap_req - total_ap} AP remaining to level.")

    def return_skill_rank(self, skillset, skill):
        """
        Looks to see if the owner posesses a specified skillset.
        Generates a dictionary specific to that skillset and adds the base and bonus ranks.
        Uses the total skillset ranks as a base rank for the skill.
        Final skill rank is a result of the skill rank added to the total skillset ranks.
        """
        skill_rank = 0
        if skillset in self.skillset_dics:
            skillset_dic = self.skillset_dics[skillset]
            skillset_base_rank = skillset_dic['base ranks']
            skillset_bonus_rank = skillset_dic['bonus ranks']
            skillset_rank = skillset_base_rank + skillset_bonus_rank
            if skill in skillset_dic:
                skill_bonus_rank = skillset_dic[skill]
                skill_rank = skillset_rank + skill_bonus_rank
        return skill_rank

    def generate_skill_list(self):
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

    
        for i in skillsets.VIABLE_SKILLSETS:
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

            if i in self.skillset_dics: # If the skillset exists on the character.
                base_ranks = self.skillset_dics[i]['base ranks']
                bonus_ranks = self.skillset_dics[i]['bonus ranks']
                skill_base_rank = base_ranks + bonus_ranks
                current_ap = self.skillset_dics[i]['current ap']
                next_rank_ap_req = self.ap_required(base_ranks + 1)
                ap_remaining = next_rank_ap_req - current_ap

                # Build skill lists
                for x in skillsets.VIABLE_SKILLS:
                    if x in self.skillset_dics[i]: # If the skill exists on the character.
                        skill_bonus_rank = self.skillset_dics[i][x] # Store that skill's bonus
                        skill_rank = self.return_skill_rank(i, x)
                        skill_difficulty = skillsets.skillsets[i][x]['difficulty']
                        skill_rank_score = self.return_rank_score(skill_rank, skill_difficulty)

                        # Store the skill's name in a list, sorted by skill type.
                        if skillsets.skillsets[i][x]['skill_type'] == 'offense':
                            offense_skill_list.append(x)
                            offense_skill_base_rank_list.append(skill_base_rank)
                            offense_skill_bonus_rank_list.append(skill_bonus_rank)
                            offense_rank_list.append(skill_rank)
                            offense_rank_score_list.append(skill_rank_score)
                        elif skillsets.skillsets[i][x]['skill_type'] == 'defense':
                            defense_skill_list.append(x)
                            defense_skill_base_rank_list.append(skill_base_rank)
                            defense_skill_bonus_rank_list.append(skill_bonus_rank)
                            defense_rank_list.append(skill_rank)
                            defense_rank_score_list.append(skill_rank_score)
                        elif skillsets.skillsets[i][x]['skill_type'] == 'utility':
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
        high_def_rs, mid_def_rs, low_def_rs = self.defense_layer_calc(rs_only=True)
        def_rs = f"\n\nCurrent total defensive RS - High: {high_def_rs}    Mid: {mid_def_rs}    Low: {low_def_rs}\n"

        result = f"{header}{full_skillsets_string}{def_rs}\n{footer}"
        return result