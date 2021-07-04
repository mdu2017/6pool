"""
File that handles damage calculations for various units
"""

import pandas as pd
import math

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


def unit_vs(curr_unit, enemy_unit_list, c_weapon_lvl, e_armor_lvl, e_shield_lvl, is_protoss):
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

    enemy_unit_names = []
    damage_to_hp = []
    damage_to_shields = []
    enemy_hp = []
    enemy_shields = []

    # Calculate damage against enemy unit and create lists for each stat
    for enemy_unit in enemy_units.itertuples(index=False, name='Unit'):
        enemy_name, damage_to_h, damage_to_s, e_hp, e_shields = calculate_dmg(curr_unit, int(c_weapon_lvl),
                                                                              enemy_unit, int(e_armor_lvl),
                                                                              int(e_shield_lvl), is_protoss)
        enemy_unit_names.append(enemy_name)
        damage_to_hp.append(damage_to_h)
        damage_to_shields.append(damage_to_s)
        enemy_hp.append(e_hp)
        enemy_shields.append(e_shields)

    unit_vs = pd.DataFrame()
    unit_vs['Enemy Unit Name'] = pd.Series(data=enemy_unit_names)
    unit_vs['Damage To HP'] = pd.Series(data=damage_to_hp)
    unit_vs['Damage To Shields'] = pd.Series(data=damage_to_shields)
    unit_vs['HP'] = pd.Series(data=enemy_hp)
    unit_vs['Shields'] = pd.Series(data=enemy_shields)

    return unit_vs


def calculate_dmg(curr_unit, curr_weapon_level, enemy_unit, enemy_armor_level, enemy_shield_level, is_protoss):
    """
    Calculates damages against another unit
    :param is_protoss: is protoss unit
    :param curr_unit: selected unit
    :param curr_weapon_level: current weapon level upgrade
    :param enemy_unit: enemy unit to compare against
    :param enemy_armor_level:  enemy armor level upgrade
    :param enemy_shield_level: enemy shield level upgrade
    :return: damage to enemy unit
    """

    # Grab enemy unit props
    enemy_unit_name = enemy_unit[0]
    enemy_unit_size = enemy_unit[1]
    enemy_hp = enemy_unit[8]
    enemy_armor = enemy_unit[10]
    enemy_status = enemy_unit[13]

    # Calculate ground and air damage with upgrades
    unit_ga_value = curr_unit.iloc[0]['Ground Attack']
    unit_aa_value = curr_unit.iloc[0]['Air Attack']

    # Enemy armor value
    enemy_armor_value = (enemy_armor + enemy_armor_level)

    # NOTE: ARMOR is factored in first, THEN unit size modifiers
    #  ex: (22 damage - 1 armor) * 0.5 damage

    # Calculate air/ground damage as needed
    if unit_aa_value != 0:
        aa_type = curr_unit.iloc[0]['Air Attack Type']
        unit_aa_mod = curr_unit.iloc[0]['Air Attack Mod']
        unit_admg = unit_aa_value + (curr_weapon_level * unit_aa_mod)
        air_dmg_to_hp = (unit_admg - enemy_armor_value)

        if aa_type == 'C':
            if enemy_unit_size == 'M':
                air_dmg_to_hp *= CONCUSSIVE_MEDIUM_MOD
            elif enemy_unit_size == 'L':
                air_dmg_to_hp *= CONCUSSIVE_LARGE_MOD
        if aa_type == 'E':
            if enemy_unit_size == 'S':
                air_dmg_to_hp *= EXPLOSIVE_SMALL_MOD
            elif enemy_unit_size == 'M':
                air_dmg_to_hp *= EXPLOSIVE_MEDIUM_MOD

    if unit_ga_value != 0:
        ga_type = curr_unit.iloc[0]['Ground Attack Type']
        unit_ga_mod = curr_unit.iloc[0]['Ground Attack Mod']
        unit_gdmg = unit_ga_value + (curr_weapon_level * unit_ga_mod)
        ground_dmg_to_hp = (unit_gdmg - enemy_armor_value)

        if ga_type == 'C':
            if enemy_unit_size == 'M':
                ground_dmg_to_hp *= CONCUSSIVE_MEDIUM_MOD
            elif enemy_unit_size == 'L':
                ground_dmg_to_hp *= CONCUSSIVE_LARGE_MOD
        if ga_type == 'E':
            if enemy_unit_size == 'S':
                ground_dmg_to_hp *= EXPLOSIVE_SMALL_MOD
            elif enemy_unit_size == 'M':
                ground_dmg_to_hp *= EXPLOSIVE_MEDIUM_MOD

    # Do shield calculations if protoss
    if is_protoss:
        enemy_shields = enemy_unit[9]
        enemy_shield_value = enemy_shield_level

        if unit_ga_value != 0:
            ground_dmg_to_shield = (unit_gdmg - enemy_shield_value)
        if unit_aa_value != 0:
            air_dmg_to_shield = (unit_admg - enemy_shield_value)

        if enemy_status == 'ground':
            return enemy_unit_name, ground_dmg_to_hp, ground_dmg_to_shield, enemy_hp, enemy_shields
        else:
            return enemy_unit_name, air_dmg_to_hp, air_dmg_to_shield, enemy_hp, enemy_shields
    else:
        # Return damage against for ground/air based on enemy status
        if enemy_status == 'ground':
            return enemy_unit_name, ground_dmg_to_hp, 0, enemy_hp, 0
        else:
            return enemy_unit_name, air_dmg_to_hp, 0, enemy_hp, 0


def calculate_HTK(enemy_unit):
    """
    Enemy unit is a dataframe that should contain name, damage against hp/shields, hp/shields
    :param enemy_unit: enemy unit to calculate HTK
    :return: modified dataframe
    """

    htk = []

    for unit in enemy_unit.itertuples(index=False, name='Unit'):
        hp_dmg = unit[1]
        shield_dmg = unit[2]

        hits = 0
        shields_remaining = unit[4]
        rem_damage = 0

        # Calculate hits to deplete shields
        while shields_remaining > 0:

            # If more damage to shields than shields remaining, add as remainder
            if (shields_remaining - shield_dmg) < 0:
                rem_damage = abs(shields_remaining - shield_dmg)

            shields_remaining -= shield_dmg
            hits += 1

        # If extra damage remains, reduce from hp
        hp_remaining = unit[3]
        if rem_damage > 0:
            hp_remaining -= rem_damage

        # Calculate hits to deplete hp
        while hp_remaining > 0:
            hp_remaining -= hp_dmg
            hits += 1

        htk.append(hits)

    enemy_unit['Hits To Kill'] = pd.Series(data=htk)

    return enemy_unit


def calculate_dmg_taken(curr_unit, enemy_units, curr_armor_level, enemy_weapon_level):
    """
    Calculates how much each enemy deals to selected unit
    :param curr_unit: selected unit
    :param enemy_units: enemy unit list
    :param curr_armor_level: current armor level
    :param enemy_weapon_level: enemy weapon level
    :return:
    """
    curr_unit_status = curr_unit.iloc[0]['Status']
    curr_armor = (curr_unit.iloc[0]['Armor'] + int(curr_armor_level))
    curr_size = curr_unit.iloc[0]['Unit Size']
    enemy_unit_list = enemy_units
    damage_to_hp = []

    # Filter out only units that can attack the selected unit
    if curr_unit_status == 'ground':
        # Need to make copy to avoid hidden chaining, also reset index to keep units in order
        enemy_unit_list = enemy_unit_list[enemy_unit_list['Ground Attack'] > 0].copy()
        attack_type_index = 6
        attack_val_index = 2
        attack_mod_index = 4
    else:
        enemy_unit_list = enemy_unit_list[enemy_unit_list['Air Attack'] > 0].copy()
        attack_type_index = 7
        attack_val_index = 3
        attack_mod_index = 5

    # Reset index to fix unit ordering
    enemy_unit_list.reset_index(drop=True, inplace=True)

    # Calculate damage dealt against unit
    for e_unit in enemy_unit_list.itertuples(index=False, name='EnemyUnit'):
        e_attack_type = e_unit[attack_type_index]
        e_attack_val = e_unit[attack_val_index]
        e_attack_mod = e_unit[attack_mod_index]
        enemy_attack = e_attack_val + (e_attack_mod * int(enemy_weapon_level))
        damage_taken = (enemy_attack - curr_armor)

        # Apply size modifiers
        if curr_size == 'S':
            if e_attack_type == 'E':
                damage_taken *= EXPLOSIVE_SMALL_MOD
        elif curr_size == 'M':
            if e_attack_type == 'E':
                damage_taken *= EXPLOSIVE_MEDIUM_MOD
            elif e_attack_type == 'C':
                damage_taken *= CONCUSSIVE_MEDIUM_MOD
        elif curr_size == 'L':
            if e_attack_type == 'C':
                damage_taken *= CONCUSSIVE_LARGE_MOD

        damage_to_hp.append(damage_taken)
        print(damage_taken)

    enemy_unit_list['HP Damage Taken'] = pd.Series(data=damage_to_hp)

    return enemy_unit_list







