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
    if display_unit_info:
        st.write(all_units)

    # Sidebar choice option for unit race
    unit_race = st.sidebar.radio(
        label='Select Unit Race',
        options=['Terran', 'Zerg', 'Protoss'])

    # Damage Charts mode
    if chart_mode == 'Damage Charts':
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
        if unit_race == 'Terran':
            options = terran_units['Unit Name']
        elif unit_race == 'Zerg':
            options = zerg_units['Unit Name']
        elif unit_race == 'Protoss':
            options = protoss_units['Unit Name']

        unit_selected = st.sidebar.selectbox(
            label='Select Unit',
            options=options
        )

    elif chart_mode == 'Table Format':
        print()


# Adjusted damage value based on attack types
def adjusted_damage():
    print()

def calculate_damage():
    print()
