# Data #1

data["Total population"]["2000"]
data["Total population"]["2000"].loc["Poland"]
# or
data["Total population"].loc["Poland", "2000"]

# Data #2

new_conf = get_config(data, "Life expectancy", "Murder per 100,000, age adjusted")
new_conf["x_df"].loc["Japan", "2000"]
