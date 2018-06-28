import os
import pandas as pd


TOTAL_POPULATION_FILE = "indicator gapminder population.xlsx"


def load_df(file_name):
    df = pd.read_excel("data/{}".format(file_name))
    df = df.set_index(df.columns[0])

    # Some files got strings, some ints, why?
    df.columns = df.columns.astype(str)
    # Aren't we dropping columns in the middle?
    df = df.dropna(axis="columns", how="all")

    return df


def load_data():
    data = {}

    population_df = load_df(TOTAL_POPULATION_FILE)

    for file_name in os.listdir("data"):
        df = load_df(file_name)

        # We analyze only countries with population
        df = df.loc[df.index.isin(population_df.index)]

        data[df.index.name] = df

    return data
