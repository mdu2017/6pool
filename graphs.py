import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import loader
import damage

"""
This file contains methods for drawing the graphs on the page

"""
CHART_WIDTH = 700
CHART_HEIGHT = 550
CHART_FONT_SIZE = 16
CHART_LABEL_SIZE = 18


# Base function for drawing chart
def draw_chart(unit_list, ga_choice, unit_size):
    # Set y axis field name based on ground and size option
    if ga_choice == 'Ground':
        title = 'Ground Attack Value'
        field_name = 'Ground Attack'
        if unit_size == 'Small':
            field_name = 'Ground vs Small'
        elif unit_size == 'Medium':
            field_name = 'Ground vs Medium'
        elif unit_size == 'Large':
            field_name = 'Ground vs Large'

    elif ga_choice == 'Air':
        title = 'Air Attack Value'
        field_name = 'Air Attack'
        if unit_size == 'Small':
            field_name = 'Air vs Small'
        elif unit_size == 'Medium':
            field_name = 'Air vs Medium'
        elif unit_size == 'Large':
            field_name = 'Air vs Large'

    # Set y values and filter
    y = alt.Y(field=field_name, title=title, type='quantitative', sort='-y')
    field_predicate = alt.FieldGTPredicate(field=field_name, gt=1)

    # Create damage chart
    chart = alt.Chart(data=unit_list).mark_bar().encode(
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
    my_chart = alt.layer(chart, text, data=unit_list).properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT
    ).configure_axis(  # Need to run configure_axis() on last chart b/c of config issue
        labelFontSize=CHART_LABEL_SIZE,
        titleFontSize=CHART_FONT_SIZE
    )

    # Display chart to page
    st.altair_chart(altair_chart=my_chart, use_container_width=True)


# Drawk hits-to-kill chart for unit
def draw_HTK_chart(curr_unit, enemy_unit_list, c_weapon_lvl, e_armor_lvl, e_shield_lvl):
    # damage.damage_HTK(curr_unit, enemy_unit_list, c_weapon_lvl, e_armor_lvl, e_shield_lvl)
    print()


if __name__ == "__main__":
    terran_units, _, _, _ = loader.load_data()
    damage.process_damage(terran_units)

    # damage.process_damage(terran_units)
    unit = terran_units[terran_units['Unit Name'] == 'Marine']
    result = damage.damage_HTK(unit, terran_units, '0', '0', '0')
    # print(result)