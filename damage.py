"""
File that handles damage calculations for various units
"""

import pandas as pd

# Modifiers for special damage types
CONCUSSIVE_MEDIUM_MOD = 0.5
CONCUSSIVE_LARGE_MOD = 0.25
EXPLOSIVE_SMALL_MOD = 0.5
EXPLOSIVE_MEDIUM_MOD = 0.75


def process_damage(unit_list):
    """
    Process and return large dataframe with modified damages columns
    :param unit_list: dataframe
    :return:
    """
    ground_damage_values = unit_list['Ground Attack']
    ground_damage_type = unit_list['Ground Attack Type']

    air_damage_values = unit_list['Air Attack']
    air_damage_type = unit_list['Air Attack Type']

    gsmall = []
    gmedium = []
    glarge = []

    asmall = []
    amedium = []
    alarge = []

    for g_dmg, g_type, a_dmg, a_type in zip(ground_damage_values, ground_damage_type,
                                            air_damage_values, air_damage_type):
        s_gr = g_dmg
        m_gr = g_dmg
        l_gr = g_dmg

        s_air = a_dmg
        m_air = a_dmg
        l_air = a_dmg

        if g_type == 'E':
            s_gr = s_gr * EXPLOSIVE_SMALL_MOD
            m_gr = m_gr * EXPLOSIVE_MEDIUM_MOD
        elif g_type == 'C':
            m_gr = m_gr * CONCUSSIVE_MEDIUM_MOD
            l_gr = l_gr * CONCUSSIVE_LARGE_MOD

        if a_type == 'E':
            s_air = s_air * EXPLOSIVE_SMALL_MOD
            m_air = m_air * EXPLOSIVE_MEDIUM_MOD
        elif a_type == 'C':
            m_air = m_air * CONCUSSIVE_MEDIUM_MOD
            l_air = l_air * CONCUSSIVE_LARGE_MOD

        gsmall.append(s_gr)
        gmedium.append(m_gr)
        glarge.append(l_gr)
        asmall.append(s_air)
        amedium.append(m_air)
        alarge.append(l_air)

    unit_list['Ground vs Small'] = pd.Series(data=gsmall)
    unit_list['Ground vs Medium'] = pd.Series(data=gmedium)
    unit_list['Ground vs Large'] = pd.Series(data=glarge)
    unit_list['Air vs Small'] = pd.Series(data=asmall)
    unit_list['Air vs Medium'] = pd.Series(data=amedium)
    unit_list['Air vs Large'] = pd.Series(data=alarge)


def damage_HTK(curr_unit, enemy_unit_list, c_weapon_lvl, e_armor_lvl, e_shield_lvl):
    """
    Calculate hits-to-kill for each unit in the list
    :param e_shield_lvl: enemy shield upgrade level
    :param e_armor_lvl:  enemy armor upgrade level
    :param c_weapon_lvl: selected unit weapon level
    :param enemy_unit_list: enemy unit list
    :param curr_unit: unit selected
    :return: dataframe with [unit names, hits_to_kill]
    """

    # Get ground and air attack values
    ga_value = curr_unit.iloc[0]['Ground Attack']
    aa_value = curr_unit.iloc[0]['Air Attack']

    # Filter out enemy units that are invulnerable to curr unit (air/ground status)
    if ga_value == 0:
        enemy_units = enemy_unit_list[enemy_unit_list['Status'] == 'air']
    elif aa_value == 0:
        enemy_units = enemy_unit_list[enemy_unit_list['Status'] == 'ground']
    else:
        enemy_units = enemy_unit_list


    # For each enemy unit, calculate damage against, factoring in weapon/armor ups, health/shields (ignore regen)
    #  dmg_to_hp = attack damage + (weapon level * attack mod) - (Enemy armor + armor level)
    #  dmg_to_shields = atk dmg + (wpn lvl * attack mod) - (shield level)
    #   total_htk = (dmg_to_shields / total_Shields) + (dmg_to_hp / hp)

    for enemy_unit in enemy_units:
        temp = calculate_dmg(curr_unit, int(c_weapon_lvl), enemy_unit, int(e_armor_lvl), int(e_shield_lvl))
        print(temp)



def calculate_dmg(curr_unit, curr_weapon_level, enemy_unit, enemy_armor_level, enemy_shield_level):
    """
    Calculates damages against another unit
    :param curr_unit: selected unit
    :param curr_weapon_level: current weapon level upgrade
    :param enemy_unit: enemy unit to compare against
    :param enemy_armor_level:  enemy armor level upgrade
    :param enemy_shield_level: enemy shield level upgrade
    :return: damage to enemy unit
    """

    # print(curr_unit)
    print(enemy_unit)

    # Take ground and air damage
    # unit_ga_value = curr_unit.iloc[0]['Ground Attack']
    # unit_aa_value = curr_unit.iloc[0]['Air Attack']
    #
    # unit_ga_mod = curr_unit.iloc[0]['Ground Attack Mod']
    # unit_aa_mod = curr_unit.iloc[0]['Air Attack Mod']
    #
    # unit_gdmg = unit_ga_value + (curr_weapon_level * unit_ga_mod)
    # unit_admg = unit_aa_value + (curr_weapon_level * unit_aa_mod)
    #
    # # Enemy armor
    # enemy_armor_value = (enemy_unit.iloc[0]['Armor'] + enemy_armor_level)
    # enemy_shield_value = (enemy_unit.iloc[0]['Shield Armor'] + enemy_shield_level)
    #
    # # Calculate damages for ground attacks
    # ground_dmg_to_hp = (unit_gdmg - enemy_armor_value)
    # ground_dmg_to_shield = (unit_gdmg - enemy_shield_value)
    #
    # # Calculate damages for air atttacks
    # air_dmg_to_hp = (unit_admg - enemy_armor_value)
    # air_dmg_to_shield = (unit_admg - enemy_shield_value)
    #
    # # return tuple of values
    # true_dmg_values = (ground_dmg_to_hp, ground_dmg_to_shield, air_dmg_to_hp, air_dmg_to_shield)
    # return true_dmg_values
