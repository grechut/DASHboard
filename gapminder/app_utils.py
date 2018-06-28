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


def get_range(values):
    min_value = values.min().min()
    max_value = values.max().max()

    range_width = max_value - min_value

    return [min_value - range_width * 0.1, max_value + range_width * 0.1]
