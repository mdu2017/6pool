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
        label='Display unit info',
        help='Displays info table for all units'
    )

    # Sidebar choice option for unit race
    selected_unit_race = st.sidebar.radio(
        label='Select Unit Race',
        options=['Terran', 'Zerg', 'Protoss'])

    # Display unit info box
    if display_unit_info:
        st.write(all_units)

    # Damage Charts mode
    if chart_mode == OPT_DMG_CHART:
        st.title('Starcraft Unit Damage Charts')

        # Display ground/air options
        ga_choice = st.radio(
            label='Select Ground/Air Attacks',
            options=['Ground', 'Air']
        )

        # Unit size option
        unit_size_choice = st.select_slider(
            label=f'Select Enemy Unit Size - Damage Against',
            options=['Base', 'Small', 'Medium', 'Large']
        )

        # Generate damage charts for terran units
        if selected_unit_race == 'Terran':
            graphs.draw_chart(terran_units, ga_choice, unit_size_choice)

            # Note for special terran units
            if ga_choice == 'Air':
                st.info('Note: Valkyries shoot 2 groups of 4 missiles for a total of 6 (x8) damage')

        # Charts for zerg units
        elif selected_unit_race == 'Zerg':
            graphs.draw_chart(zerg_units, ga_choice, unit_size_choice)

            # Note for special zerg units
            if ga_choice == 'Ground':
                st.info('Note: Infested Terrans are left off the chart due to rarity of use.')

        # Charts for protoss units
        elif selected_unit_race == 'Protoss':
            graphs.draw_chart(protoss_units, ga_choice, unit_size_choice)

            if ga_choice == 'Ground':
                st.info('Zealots do 2 attacks for a total of 8 (x2) damage')
            if ga_choice == 'Air':
                st.info('''Note: Carriers can build up to 8 interceptors dealing 6 (x8) damage.''')

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
            st.title('Unit Damage Dealt')

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
            shield_note = 'Note: Protoss shields will take full damage from any attack, regardless of size'


            # Display graphs
            st.subheader(f'{unit_selected} vs {enemy_unit_race} Units')

            # Draw graph for selected mode
            if chart_option == 'Damage Against':
                graphs.draw_unit_vs(unit_vs)
                st.info(shield_note)
            elif chart_option == 'Hits to Kill':
                graphs.draw_HTK(unit_HTK)
                st.info(htk_note)

        elif chart_mode == OPT_UNIT_TAKEN:

            st.title('Unit Damage Taken')

            # Selected weapon and armor upgrade levels
            c_armor_level = st.sidebar.select_slider(label='Selected unit armor level', options=['0', '1', '2', '3'])
            if selected_unit_race == PROTOSS_NAME:
                c_shield_level = st.sidebar.select_slider(
                    label='Selected unit shield level', options=['0', '1', '2', '3']
                )
            e_weapon_level = st.sidebar.select_slider(label='Enemy weapon upgrade level', options=['0', '1', '2', '3'])

            st.subheader(f'{unit_selected} damage taken from {enemy_unit_race} units')

            graphs.draw_damage_taken(curr_unit, enemy_list, c_armor_level, e_weapon_level)
            st.info('Note: Protoss Shields take full damage from all attack types')

