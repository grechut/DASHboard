import numpy as np

# Very much POC, rethink.
# Prolly we need log as it will display more fair
class MarkerSize:
    def __init__(self, values, max_size=40, min_size=10):
        self.min_val = values.min()
        self.max_val = values.max()
        self.max_size = max_size
        self.min_size = min_size

    def size(self, value):
        scaled = (value - self.min_val) / self.max_val
        return self.min_size + scaled * (self.max_size - self.min_size)


def options(keys):
    return [{"label": k, "value": k} for k in keys]


def get_axis(values):
    min_value = values.min().min()
    max_value = values.max().max()

    axis_type = "log" if max_value > 1e5 and min_value > 0 else "linear"

    if axis_type == "log":
        min_value = np.log10(min_value)
        max_value = np.log10(max_value)

    range_width = max_value - min_value

    if axis_type == "linear":
        # Log cannot be < 0
        min_value = min_value - range_width * 0.1

    return {"range": [min_value, max_value + range_width * 0.1], "type": axis_type}
