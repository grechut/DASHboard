import os
import pandas as pd


def load_data():
    data = {}

    for f in os.listdir("data"):
        df = pd.read_excel("data/{}".format(f))
        df = df.set_index(df.columns[0])
        # Some files got strings, some ints, why?
        df.columns = df.columns.astype(str)
        data[df.index.name] = df

    return data
