from loader import load_data
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from altair import datum
from vega_datasets import data
import graphs
import loader
import damage
from graphs import *

if __name__ == '__main__':

    # Load in dataset
    terran_units, zerg_units, protoss_units, all_units = loader.load_data()

    # Process damages
    damage.process_damage(terran_units)
    damage.process_damage(zerg_units)
    damage.process_damage(protoss_units)

    # Chart mode selection box
    chart_mode = st.sidebar.selectbox(
        label='Select Chart Mode',
        options=[OPT_DMG_CHART, OPT_UNIT_DAMAGE, OPT_UNIT_TAKEN]
    )

    # Display unit info table - checkbox
    display_unit_info = st.sidebar.checkbox(
        label='Display all unit info',
        help='Displays info table for all units'
    )

    # Display unit info box
    if display_unit_info:
        st.write(all_units)

    # Sidebar choice option for unit race
    selected_unit_race = st.sidebar.radio(
        label='Select Unit Race',
        options=['Terran', 'Zerg', 'Protoss'])

    # Sort option
    sort_opt = st.sidebar.radio(label='Sort By:', options=['Increasing', 'Decreasing'])
    if sort_opt == 'Increasing':
        sort_y = 'y'
    else:
        sort_y = '-y'

    st.title('Starcraft Unit Damage Statistics')

    # Chart mode title
    st.subheader(chart_mode)

    # Damage Charts mode
    if chart_mode == OPT_DMG_CHART:

        # Display ground/air options
        ga_choice = st.radio(
            label='Select Ground/Air Attacks',
            options=['Ground', 'Air']
        )

        # Unit size option
        unit_size_choice = st.radio(
            label=f'Select Enemy Unit Size',
            options=['Base', 'Small', 'Medium', 'Large']
        )

        st.subheader(f'Damage Against {ga_choice} units')

        # Generate damage charts for terran units
        if selected_unit_race == 'Terran':
            graphs.draw_chart(terran_units, ga_choice, unit_size_choice, sort_y)

            # Note for special terran units
            if ga_choice == 'Air':
                st.info('Note: Valkyries shoot 2 groups of 4 missiles for a total of 6 (x8) damage')
                st.info('Note: Goliaths shoot 2 missile for a total of 10 (x2) damage')

        # Charts for zerg units
        elif selected_unit_race == 'Zerg':
            graphs.draw_chart(zerg_units, ga_choice, unit_size_choice, sort_y)

            # Note for special zerg units
            if ga_choice == 'Ground':
                st.info('Note: Infested Terrans are left off the chart due to rarity of use.')

        # Charts for protoss units
        elif selected_unit_race == 'Protoss':
            graphs.draw_chart(protoss_units, ga_choice, unit_size_choice, sort_y)

            if ga_choice == 'Ground':
                st.info('Zealots hit twice for a total of 8 (x2) damage')
            if ga_choice == 'Air':
                st.info('''Note: Carriers can build up to 8 interceptors dealing 6 (x8) damage.''')
                st.info('Note: Scouts hit twice for a total of 14 (x2) damage')

    # Unit damage dealt chart mode
    else:

        # Filter units by race
        filtered_units, options = loader.assign_unit_option(selected_unit_race, terran_units, zerg_units, protoss_units)

        # Unit selected on sidebar choice
        unit_selected = st.sidebar.selectbox(label='Select Unit', options=options)
        curr_unit = filtered_units[filtered_units['Unit Name'] == unit_selected]

        # Select enemy unit race on page
        enemy_unit_race = st.radio(label='Select Enemy Unit Race', options=['Terran', 'Zerg', 'Protoss'])

        # Select appropriate enemy list
        if enemy_unit_race == TERRAN_NAME:
            enemy_list = terran_units
            htk_note = 'Note: Terran units can be healed or repaired, which may affect these numbers'
        elif enemy_unit_race == ZERG_NAME:
            enemy_list = zerg_units
            htk_note = 'Note: Zerg units have health regeneration, which may affect these numbers'
        else:
            enemy_list = protoss_units
            htk_note = 'Note: Protoss units have shield regeneration, which may affect these numbers'

        if chart_mode == OPT_UNIT_DAMAGE:

            # Selected weapon and armor upgrade levels
            curr_weapon_level = st.sidebar.select_slider(label='Weapon upgrade level', options=['0', '1', '2', '3'])
            enemy_armor_level = st.sidebar.select_slider(label='Enemy armor level', options=['0', '1', '2', '3'])
            if enemy_unit_race == 'Protoss':
                enemy_shield_level = st.sidebar.select_slider(
                    label='Enemy shield level', options=['0', '1', '2', '3']
                )
                is_protoss = True
            else:
                enemy_shield_level = '0'
                is_protoss = False

            # Chart choice option
            chart_option = st.radio(label='Show: ', options=['Damage Against', 'Hits to Kill'])

            # Processed damage list for enemy list
            unit_vs = damage.unit_vs(curr_unit, enemy_list,
                                     curr_weapon_level, enemy_armor_level, enemy_shield_level, is_protoss)
            unit_HTK = damage.calculate_HTK(curr_unit, unit_vs)

            loader.append_size_suffix(unit_vs, 'Enemy Unit Name')
            loader.append_size_suffix(unit_HTK, 'Enemy Unit Name')
            shield_note = 'Note: Protoss shields will take full damage from any attack, regardless of size'

            # Display graphs
            st.subheader(f'{unit_selected} vs {enemy_unit_race} Units')

            # Draw graph for selected mode
            if chart_option == 'Damage Against':
                graphs.draw_unit_vs(unit_vs, sort_y)
                st.info(shield_note)
            elif chart_option == 'Hits to Kill':
                graphs.draw_HTK(unit_HTK, sort_y)
                st.info(htk_note)

        elif chart_mode == OPT_UNIT_TAKEN:

            # Selected weapon and armor upgrade levels
            c_armor_level = st.sidebar.select_slider(label='Selected unit armor level', options=['0', '1', '2', '3'])
            if selected_unit_race == PROTOSS_NAME:
                c_shield_level = st.sidebar.select_slider(
                    label='Selected unit shield level', options=['0', '1', '2', '3']
                )
            e_weapon_level = st.sidebar.select_slider(label='Enemy weapon upgrade level', options=['0', '1', '2', '3'])

            st.subheader(f'{unit_selected} damage taken from {enemy_unit_race} units')

            # Processed dataframe with damage taken values
            dmg_taken = damage.calculate_dmg_taken(curr_unit, enemy_list, c_armor_level, e_weapon_level)

            graphs.draw_damage_taken(dmg_taken, sort_y)
            st.info('Note: Protoss Shields take full damage from all attack types')

