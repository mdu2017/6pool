from loader import load_data
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from altair import datum
from vega_datasets import data

if __name__ == '__main__':

    CHART_WIDTH = 700
    CHART_HEIGHT = 550

    # Dataframes
    terran_units = pd.read_csv('./data/terran_units.csv', sep=',', header=0)
    zerg_units = pd.read_csv('./data/zerg_units.csv', sep=',', header=0)
    protoss_units = pd.read_csv('./data/protoss_units.csv', sep=',', header=0)

    # Join into 1 large list for info table
    all_units = pd.concat(
        [terran_units, zerg_units, protoss_units],
        axis=0,
        join="outer",
        ignore_index=True,
        keys=None,
        levels=None,
        names=None,
        verify_integrity=False,
        copy=True,
    )

    st.title('Starcraft Unit Damage Stats')

    # TODO: Selectbox for mode (Damage charts, Damage Against, Table format)
    st.sidebar.selectbox(
        label='Select Chart Mode',
        options=['Damage Charts', 'Damage Against', 'Table Format']
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

    if unit_race == 'Terran':

        ga_choice = st.radio(
            label='Select Ground/Air Attacks',
            options=['Ground', 'Air']
        )

        # TODO: damage calculations for different enemy sizes
        unit_size_choice = st.select_slider(
            label=f'Select Enemy Unit Size - Damage Against',
            options=['Base', 'Small', 'Medium', 'Large']
        )


        # Set y axis based on ground/air option selected
        if ga_choice == 'Ground':
            y = alt.Y(field='Ground Attack', title='Ground Attack Value', type='quantitative', sort='-y')
            field_predicate = alt.FieldGTPredicate(field='Ground Attack', gt=1)
        else:
            y = alt.Y(field='Air Attack', title='Air Attack Value', type='quantitative', sort='-y')
            field_predicate = alt.FieldGTPredicate(field='Air Attack', gt=1)

        # Create damage chart
        chart = alt.Chart(data=terran_units).mark_bar().encode(
            x=alt.X(field='Unit Name', title='Unit Name', type='nominal'),
            y=y,
            color=alt.condition(
                alt.FieldEqualPredicate(field='Unit Name', equal='Valkyrie'),
                alt.value('coral'),  # which sets the bar orange.
                alt.value('steelblue')  # And if it's not true it sets the bar steelblue.
            )
        ).transform_filter(
            field_predicate
        )

        # Bar chart labels
        text = chart.mark_text(
            align='center',
            baseline='middle',
            dy=-5
        ).encode(
            text=y.field  # This has to match a column name
        )

        # Add base chart and text to layered chart for labels
        my_chart = alt.layer(chart, text, data=terran_units).properties(
            width=CHART_WIDTH,
            height=CHART_HEIGHT
        ).configure_axis(       # Need to run configure_axis() on last chart b/c of config issue
            labelFontSize=16,
            titleFontSize=18
        )

        # Display chart to page
        st.altair_chart(altair_chart=my_chart, use_container_width=True)

        if ga_choice == 'Air':
            st.info('Note: Valkyries shoot 2 groups of 4 missiles for a total of 6 (x8) damage')

    elif unit_race == 'Zerg':
        st.write(zerg_units)
    elif unit_race == 'Protoss':
        st.write(protoss_units)

# Adjusted damage value based on attack types
def adjusted_damage():
    print()

def calculate_damage():
    print()
