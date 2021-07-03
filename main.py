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
        options=['Damage Charts', 'Unit Statistics', 'Table Format']
    )

    # Display unit info table
    display_unit_info = st.sidebar.checkbox(
        label='Display unit info',
        help='Displays info table for all units'
    )

    # Sidebar choice option for unit race
    unit_race = st.sidebar.radio(
        label='Select Unit Race',
        options=['Terran', 'Zerg', 'Protoss'])

    # Damage Charts mode
    if chart_mode == 'Damage Charts':
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
        if unit_race == 'Terran':
            graphs.draw_chart(terran_units, ga_choice, unit_size_choice)

            # Note for special terran units
            if ga_choice == 'Air':
                st.info('Note: Valkyries shoot 2 groups of 4 missiles for a total of 6 (x8) damage')

        # Charts for zerg units
        elif unit_race == 'Zerg':
            graphs.draw_chart(zerg_units, ga_choice, unit_size_choice)

        # Charts for protoss units
        elif unit_race == 'Protoss':
            graphs.draw_chart(protoss_units, ga_choice, unit_size_choice)

    elif chart_mode == 'Unit Statistics':
        st.title('Unit Statistics - Hits to Kill')

        # Display data table of units
        if display_unit_info:
            st.write(all_units)

        # Filter units by race
        if unit_race == 'Terran':
            filtered_units = terran_units[(terran_units['Ground Attack'] > 0) | (terran_units['Air Attack'] > 0)]
        elif unit_race == 'Zerg':
            filtered_units = zerg_units[(zerg_units['Ground Attack'] > 0) | (zerg_units['Air Attack'] > 0)]
        elif unit_race == 'Protoss':
            filtered_units = protoss_units[(protoss_units['Ground Attack'] > 0) | (protoss_units['Air Attack'] > 0)]

        filtered_units.reset_index(drop=True, inplace=True)  # Need to reset index after filtering, or throws key error
        options = filtered_units['Unit Name']

        # Unit selected on sidebar choice
        unit_selected = st.sidebar.selectbox(label='Select Unit', options=options)

        # Main page section
        enemy_unit_race = st.radio(label='Select Enemy Unit Race', options=['Terran', 'Zerg','Protoss'])

        # Selected weapon and armor upgrade levels
        weapon_level = st.select_slider(label='Weapon upgrade level', options=['0', '1', '2', '3'])
        armor_level = st.select_slider(label='Enemy armor level', options=['0', '1', '2', '3'])

        # Chart choice option
        chart_option = st.radio(label='Show: ', options=['Hits To Kill', 'Damage Against'])

        if enemy_unit_race == 'Terran':
            curr_unit = terran_units[terran_units['Unit Name'] == unit_selected]
            graphs.draw_HTK_chart(curr_unit, terran_units, weapon_level, armor_level, '0')
        elif enemy_unit_race == 'Zerg':
            st.write('zerg')
        elif enemy_unit_race == 'Protoss':
            shield_level = st.select_slider(
                label='Enemy shield level', options=['0', '1', '2', '3']
            )
            st.write('Protoss')


        # Below Graph:
        st.info('note below graph')

    elif chart_mode == 'Table Format':
        print()
        if display_unit_info:
            st.write(all_units)


# Adjusted damage value based on attack types
def adjusted_damage():
    print()

def calculate_damage():
    print()
