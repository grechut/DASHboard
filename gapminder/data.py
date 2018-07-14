import os
import functools

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
        df = load_df(file_name)
        data[df.index.name] = df

    return data


# Caching needs hashable stuff.
def make_stuff_hashable(func):
    class HDict(dict):
        def __hash__(self):
            # DFs are not hashable. Use Keys.
            return hash(frozenset(self.keys()))

    class HList(list):
        def __hash__(self):
            return hash(" ".join([str(x) for x in self]))

    def _make_hashable(stuff):
        if isinstance(stuff, dict):
            return HDict(stuff)
        elif isinstance(stuff, list):
            return HList(stuff)
        return stuff

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        args = tuple([_make_hashable(arg) for arg in args])
        kwargs = {k: _make_hashable(v) for k, v in kwargs.items()}
        return func(*args, **kwargs)

    return wrapped


@make_stuff_hashable
@functools.lru_cache(maxsize=32)
def get_config(data, x_axis, y_axis, z_axis=TOTAL_POPULATION, countries=None):
    x_df = data[x_axis].copy()
    y_df = data[y_axis].copy()
    z_df = data[z_axis].copy()

    dataset_countries = x_df.index.intersection(y_df.index).intersection(z_df.index)
    if countries:
        dataset_countries = dataset_countries.intersection(countries)

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
