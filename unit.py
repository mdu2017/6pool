"""
This is the class definition for a Starcraft Unit
 - Note: Some unit properties have been left out since they are not used (range, sight, etc)
"""

import csv
import json

class Unit:

    def __init__(self, props):
        """
        Loads in list of properties for each unit
        :param props: List of attributes for each unit
        """
        self.name = props[0]
        self.size = props[1]
        self.ground_attack = props[2]
        self.air_attack = props[3]
        self.gmod = props[4]
        self.amod = props[5]
        self.ga_type = props[6]  # ground attack type
        self.aa_type = props[7]  # air attack type
        self.hp = props[8]
        self.shields = props[9]
        self.armor = props[10]
        self.shield_armor = props[11]  # shield armor
        self.splash_damage = props[12]
        self.unit_type = props[13]  # This is for air/ground

    def print_unit(self):
        print(f'''Name: {self.name}, Size: {self.size}, Ground Attack: {self.ground_attack},
            Air Attack: {self.air_attack}, HP: {self.hp}, Shields: {self.shields}, Armor: {self.armor},
            Splash: {self.splash_damage}, Unit Type: {self.unit_type}''')










