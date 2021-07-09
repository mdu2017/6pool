import csv
import pandas as pd
import streamlit as st

"""
This file contains functions for loading and filtering the data
"""


@st.cache(allow_output_mutation=True)
def load_data():
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

    terran_units['Unit Names'] = terran_units['Unit Name'] + ' (' + terran_units['Unit Size'] + ')'
    zerg_units['Unit Names'] = zerg_units['Unit Name'] + ' (' + zerg_units['Unit Size'] + ')'
    protoss_units['Unit Names'] = protoss_units['Unit Name'] + ' (' + protoss_units['Unit Size'] + ')'

    return terran_units, zerg_units, protoss_units, all_units


@st.cache
def assign_unit_option(unit_race, terran_units, zerg_units, protoss_units):
    if unit_race == 'Terran':
        filtered_units = terran_units[(terran_units['Ground Attack'] > 0) | (terran_units['Air Attack'] > 0)]
    elif unit_race == 'Zerg':
        filtered_units = zerg_units[(zerg_units['Ground Attack'] > 0) | (zerg_units['Air Attack'] > 0)]
    elif unit_race == 'Protoss':
        filtered_units = protoss_units[(protoss_units['Ground Attack'] > 0) | (protoss_units['Air Attack'] > 0)]

    filtered_units.reset_index(drop=True, inplace=True)  # Need to reset index after filtering, or throws key error
    options = filtered_units['Unit Name']

    return filtered_units, options


def append_size_suffix(df, column_name):
    df['Unit Names'] = df[column_name] + ' (' + df['Unit Size'] + ')'
