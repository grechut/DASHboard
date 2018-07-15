import os
import pandas as pd


TOTAL_POPULATION = "Total population"


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

    for file_name in os.listdir("data"):
        if ".xlsx" not in file_name:
            continue

        df = load_df(file_name)
        data[df.index.name] = df

    return data


def get_config(data, x_axis, y_axis, z_axis=TOTAL_POPULATION):
    x_df = data[x_axis].copy()
    y_df = data[y_axis].copy()
    z_df = data[z_axis].copy()

    dataset_countries = x_df.index.intersection(y_df.index).intersection(z_df.index)

    years = x_df.columns.intersection(y_df.columns).intersection(z_df.columns)
    not_null = (
        (x_df.loc[dataset_countries, years].notnull())
        & (y_df.loc[dataset_countries, years].notnull())
        & (z_df.loc[dataset_countries, years].notnull())
    )

    dataset_countries = dataset_countries[not_null.any(axis="columns")]
    years = years[not_null.any(axis="rows")]

    return {
        "countries": dataset_countries.tolist(),
        "years": years.tolist(),
        "x_df": x_df.loc[dataset_countries, years],
        "y_df": y_df.loc[dataset_countries, years],
        "z_df": z_df.loc[dataset_countries, years],
    }
