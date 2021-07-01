import csv
import pandas as pd

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

    return terran_units, zerg_units, protoss_units, all_units
