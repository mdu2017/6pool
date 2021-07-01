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

    st.title('Starcraft Unit Damage Stats')

    # TODO: Selectbox for mode (Damage charts, Damage Against, Table format)
    st.sidebar.selectbox(
        label='Select Chart Mode',
        options=['Damage Charts', 'Damage Against', 'Table Format']
    )

    # TODO: option to hide non-combat units
    st.sidebar.checkbox(
        label='Hide worker and non-combat units',
    )

    # Sidebar choice option for unit race
    unit_race = st.sidebar.radio(
        label='Select Unit Race',
        options=['Terran', 'Zerg', 'Protoss'])

    if unit_race == 'Terran':

        ga_choice = st.radio(
            label='Select Ground/Air Attacks',
            options=['Ground', 'Air']
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
            y=y
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

        st.altair_chart(altair_chart=my_chart, use_container_width=True)


    elif unit_race == 'Zerg':
        st.write(zerg_units)
    elif unit_race == 'Protoss':
        st.write(protoss_units)

    # st.button('Hit me')
    # st.checkbox('Check me out')
    # st.radio('Radio', [1, 2, 3])
    # st.selectbox('Select', [1, 2, 3])
    # st.multiselect('Multiselect', [1, 2, 3])
    # st.slider('Slide me', min_value=0, max_value=10)
    # st.select_slider('Slide to select', options=[1, '2'])
    # st.text_input('Enter some text')
    # st.number_input('Enter a number')
    # st.text_area('Area for textual entry')
    # st.date_input('Date input')
    # st.time_input('Time entry')
    # st.file_uploader('File uploader')
    # st.color_picker('Pick a color')
