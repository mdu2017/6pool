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

    # TODO: Selectbox for mode (Damage charts, Damage Against, Table format)
    chart_mode = st.sidebar.selectbox(
        label='Select Chart Mode',
        options=[OPT_DMG_CHART, OPT_UNIT_DAMAGE, OPT_UNIT_TAKEN]
    )

    # Display unit info table
    display_unit_info = st.sidebar.checkbox(
        label='Display unit info',
        help='Displays info table for all units'
    )

    # Sidebar choice option for unit race
    selected_unit_race = st.sidebar.radio(
        label='Select Unit Race',
        options=['Terran', 'Zerg', 'Protoss'])

    # Damage Charts mode
    if chart_mode == OPT_DMG_CHART:
        st.title('Starcraft Unit Damage Charts')

        if display_unit_info:
            st.write(all_units)

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

            if ga_choice == 'Air':
                st.info('Note: Carriers can build up to 8 interceptors dealing 6 (x8) damage')

    # Unit damage dealt chart mode
    elif chart_mode == OPT_UNIT_DAMAGE:
        st.title('Unit Damage Dealt')

        # Display data table of units
        if display_unit_info:
            st.write(all_units)

        # Filter units by race
        filtered_units, options = loader.assign_unit_option(selected_unit_race, terran_units, zerg_units, protoss_units)

        # Unit selected on sidebar choice
        unit_selected = st.sidebar.selectbox(label='Select Unit', options=options)
        curr_unit = filtered_units[filtered_units['Unit Name'] == unit_selected]

        # Main page section
        enemy_unit_race = st.radio(label='Select Enemy Unit Race', options=['Terran', 'Zerg','Protoss'])

        # Selected weapon and armor upgrade levels
        weapon_level = st.sidebar.select_slider(label='Weapon upgrade level', options=['0', '1', '2', '3'])
        armor_level = st.sidebar.select_slider(label='Enemy armor level', options=['0', '1', '2', '3'])
        if enemy_unit_race == 'Protoss':
            shield_level = st.sidebar.select_slider(
                label='Enemy shield level', options=['0', '1', '2', '3']
            )

        # Chart choice option
        chart_option = st.radio(label='Show: ', options=['Damage Against', 'Hits to Kill'])

        st.subheader(f'{unit_selected} vs {enemy_unit_race} Units')

        if chart_option == 'Damage Against':
            if enemy_unit_race == 'Terran':
                graphs.draw_unit_vs(curr_unit, terran_units, weapon_level, armor_level, '0')
            elif enemy_unit_race == 'Zerg':
                graphs.draw_unit_vs(curr_unit, zerg_units, weapon_level, armor_level, '0')
            elif enemy_unit_race == 'Protoss':
                graphs.draw_unit_vs(curr_unit, protoss_units, weapon_level, armor_level, shield_level)
                st.info('Note: Protoss shields will take full damage from any attack, regardless of size')
        elif chart_option == 'Hits to Kill':
            if enemy_unit_race == 'Terran':
                graphs.draw_HTK(curr_unit, terran_units, weapon_level, armor_level, '0')
                st.info('Note: Terran Units can be healed/repaired')
            elif enemy_unit_race == 'Zerg':
                graphs.draw_HTK(curr_unit, zerg_units, weapon_level, armor_level, '0')
                st.info('Note: Zerg units have health regeneration, which may affect these numbers')
            elif enemy_unit_race == 'Protoss':
                graphs.draw_HTK(curr_unit, protoss_units, weapon_level, armor_level, shield_level)
                st.info('Note: Protoss units have shield regeneration, which may affect these numbers')

    elif chart_mode == OPT_UNIT_TAKEN:

        st.title('Unit Damage Taken')

        # Display data table of units
        if display_unit_info:
            st.write(all_units)

        # Filter units by race
        filtered_units, options = loader.assign_unit_option(selected_unit_race, terran_units, zerg_units, protoss_units)

        # Unit selected on sidebar choice
        unit_selected = st.sidebar.selectbox(label='Select Unit', options=options)
        curr_unit = filtered_units[filtered_units['Unit Name'] == unit_selected]

        # Main page section
        enemy_unit_race = st.radio(label='Select Enemy Unit Race', options=['Terran', 'Zerg', 'Protoss'])

        # Selected weapon and armor upgrade levels
        c_armor_level = st.sidebar.select_slider(label='Selected unit armor level', options=['0', '1', '2', '3'])
        if selected_unit_race == PROTOSS_NAME:
            c_shield_level = st.sidebar.select_slider(
                label='Selected unit shield level', options=['0', '1', '2', '3']
            )
        e_weapon_level = st.sidebar.select_slider(label='Enemy weapon upgrade level', options=['0', '1', '2', '3'])

        st.subheader(f'{unit_selected} damage taken from {selected_unit_race} units')

        if enemy_unit_race == TERRAN_NAME:
            graphs.draw_damage_taken(curr_unit, terran_units, c_armor_level, e_weapon_level)
        elif enemy_unit_race == ZERG_NAME:
            graphs.draw_damage_taken(curr_unit, zerg_units, c_armor_level, e_weapon_level)
        else:
            graphs.draw_damage_taken(curr_unit, protoss_units, c_armor_level, e_weapon_level)
            st.info('Note: Protoss Shields take full damage from all attack types')

