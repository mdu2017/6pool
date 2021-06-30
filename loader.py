import csv
from unit import Unit


def load_data():
    protoss_units = []
    zerg_units = []
    terran_units = []

    with open('./data/protoss_units.csv') as protoss_file:
        for line in csv.reader(protoss_file):
            protoss_units.append(Unit(line))

    with open('./data/zerg_units.csv') as zerg_file:
        for line in csv.reader(zerg_file):
            zerg_units.append(Unit(line))

    with open('./data/terran_units.csv') as terran_file:
        for line in csv.reader(terran_file):
            terran_units.append(Unit(line))

    return protoss_units, zerg_units, terran_units
