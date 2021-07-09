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

BAR_COLOR = 'steelblue'
# BAR_COLOR = '#82CEB7'
BAR_HIGHLIGHT_COLOR = 'coral'
# GRAPH_TEXT_COLOR = '#FFFFFF'
GRAPH_TEXT_COLOR = '#000000'

OPT_DMG_CHART = 'Unit Damage Charts'
OPT_UNIT_DAMAGE = 'Unit Damage Dealt'
OPT_UNIT_TAKEN = 'Unit Damage Taken'
TERRAN_NAME = 'Terran'
ZERG_NAME = 'Zerg'
PROTOSS_NAME = 'Protoss'

structures = ['Missile Turret', 'Spore Colony', 'Sunken Colony', 'Photon Cannon']


# Base function for drawing chart
def draw_chart(unit_list, ga_choice, unit_size, sort_opt):
    """
    Draw damage charts for units
    :param unit_list: unit list
    :param ga_choice: ground/air attack option
    :param unit_size: enemy size option
    :param sort_opt: sorting filter
    :return: graph of unit damages
    """

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

    # Set filters (remove all zero value attack units)
    field_predicate = alt.FieldGTPredicate(field=field_name, gt=1)

    # Create base chart with data
    chart = alt.Chart(data=unit_list).mark_bar().encode(
        # Sort needs to be done on x-axis (the axis being sorted), by y value
        x=alt.X(field='Unit Name', title='Unit Name', type='nominal', sort=sort_opt),
        y=alt.Y(field=field_name, title=title, type='quantitative'),
    ).transform_filter(
        field_predicate
    )

    # Set options for the bars
    bars = chart.mark_bar().encode(
        color=alt.condition(
            alt.FieldOneOfPredicate(field='Unit Name', oneOf=structures),
            alt.value(BAR_HIGHLIGHT_COLOR),  # which sets the bar orange.
            alt.value(BAR_COLOR)  # otherwise, sets bar to selected color (bluish)
        )
    )

    # Text labels for bar
    text = chart.mark_text(
        align='center',
        baseline='middle',
        dy=-5,
        color=GRAPH_TEXT_COLOR
    ).encode(
        text=field_name  # This has to match a column name
    )

    # Add base chart and text to layered chart for labels
    my_chart = alt.layer(chart, bars, text, data=unit_list).properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT
    ).configure_axis(  # Need to run configure_axis() on last chart b/c of config issue
        labelFontSize=CHART_LABEL_SIZE,
        titleFontSize=CHART_FONT_SIZE
    )

    # Display chart to page
    st.altair_chart(altair_chart=my_chart, use_container_width=True)


# Draw selected unit vs enemy units
def draw_unit_vs(unit_vs_data, sort_opt):
    """
    Draws graph for selected unit vs enemy units
    :param unit_vs_data: processed data
    :param sort_opt: ascending/descending graph
    :return: graph for unit vs
    """

    # sort_col = unit_vs_data['Damage To HP'].values.tolist()
    # sort_col.sort(reverse=True)

    # Create graph
    chart = alt.Chart(data=unit_vs_data).mark_bar().encode(
        x=alt.X(field='Enemy Unit Name', title='Enemy Unit Name', type='nominal', sort=sort_opt),
        y=alt.Y(field='Damage To HP', title='Damage to HP', type='quantitative'),
    )

    # Bars
    # TODO: bug with sorting values if color column is used
    bars = chart.mark_bar().encode(
        # color=alt.Color(field='Color', type='nominal')
        color=alt.Color(field='Color', type='nominal', scale=None)
    )

    # Bar chart labels
    text = chart.mark_text(
        align='center',
        baseline='middle',
        dy=-5,
        color=GRAPH_TEXT_COLOR
    ).encode(
        text='Damage To HP'  # This has to match a column name
    )

    # Add base chart and text to layered chart for labels
    unit_vs_chart = alt.layer(chart, bars, text, data=unit_vs_data).properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT
    ).configure_axis(  # Need to run configure_axis() on last chart b/c of config issue
        labelFontSize=CHART_LABEL_SIZE,
        titleFontSize=CHART_FONT_SIZE
    )

    # Display chart to page
    st.altair_chart(altair_chart=unit_vs_chart, use_container_width=True)


def draw_HTK(htk_data, sort_opt):
    """
    Draw hits-to-kill for enemy units in the list
    :param htk_data: processed data
    :param sort_opt: sort option ascending/descending
    :return: graph of hits-to-kill data
    """

    # Create graph
    chart = alt.Chart(data=htk_data).mark_bar().encode(
        x=alt.X(field='Enemy Unit Name', title='Enemy Unit Name', type='nominal', sort=sort_opt),
        y=alt.Y(field='Hits To Kill', title='Hits to Kill', type='quantitative'),
    )

    # Bars
    # TODO: bug with sorting -> also if scale is used, colors are wrong
    bars = chart.mark_bar().encode(
        color=alt.Color(field='Color', type='nominal', scale=None)
    )

    # Bar chart labels
    text = chart.mark_text(
        align='center',
        baseline='middle',
        dy=-5,
        color=GRAPH_TEXT_COLOR
    ).encode(
        text='Hits To Kill'  # This has to match a column name
    )

    # Add base chart and text to layered chart for labels
    unit_HTK_chart = alt.layer(chart, bars, text, data=htk_data).properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT
    ).configure_axis(  # Need to run configure_axis() on last chart b/c of config issue
        labelFontSize=CHART_LABEL_SIZE,
        titleFontSize=CHART_FONT_SIZE
    )

    # Display chart to page
    st.altair_chart(altair_chart=unit_HTK_chart, use_container_width=True)


def draw_damage_taken(curr_unit, enemy_unit_list, c_armor_level, e_weapon_level, sort_opt):
    """
    Draws graph for damage taken from other units
    :param curr_unit: selected unit
    :param enemy_unit_list: enemy units
    :param c_armor_level: selected unit's armor level
    :param e_weapon_level: enemy weapon level
    :param sort_opt: sort option
    :return: graph for damage taken
    """
    dmg_taken = damage.calculate_dmg_taken(curr_unit, enemy_unit_list, c_armor_level, e_weapon_level)

    # Create graph
    chart = alt.Chart(data=dmg_taken).mark_bar(
        color=BAR_COLOR
    ).encode(
        x=alt.X(field='Unit Name', title='Enemy Unit Name', type='nominal', sort=sort_opt),
        y=alt.Y(field='HP Damage Taken', title='HP Damage Taken From', type='quantitative'),
    )

    # Bar chart labels
    text = chart.mark_text(
        align='center',
        baseline='middle',
        dy=-5,
        color=GRAPH_TEXT_COLOR
    ).encode(
        text='HP Damage Taken'  # This has to match a column name
    )

    # Add base chart and text to layered chart for labels
    damage_taken_chart = alt.layer(chart, text, data=dmg_taken).properties(
        width=CHART_WIDTH,
        height=CHART_HEIGHT
    ).configure_axis(  # Need to run configure_axis() on last chart b/c of config issue
        labelFontSize=CHART_LABEL_SIZE,
        titleFontSize=CHART_FONT_SIZE
    )

    # Display chart to page
    st.altair_chart(altair_chart=damage_taken_chart, use_container_width=True)


# Used for debugging
# if __name__ == "__main__":
#     terran_units, zerg_units, protoss_units, _ = loader.load_data()
#     # damage.process_damage(terran_units)
#
#     # damage.process_damage(terran_units)
#     curr_unit = protoss_units[protoss_units['Unit Name'] == 'Zealot']
#     # enemy_unit = protoss_units[protoss_units['Unit Name'] == 'Zealot']
#     unit_vs = damage.unit_vs(curr_unit, zerg_units, 0, 3, 0, False)
#     # print(unit_vs)
#     enemy_htk = damage.calculate_HTK(curr_unit, unit_vs)
#
#     pd.set_option('display.max_columns', None)
#     print(enemy_htk)
