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
