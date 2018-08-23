# Data for dashboard

life_murder_conf = get_config(
    data, "Life expectancy", "Murder per 100,000, age adjusted"
)
life_murder_conf["x_df"].loc["Japan", "2000"]

# First graphs

X_AXIS = "Life expectancy"
Y_AXIS = "Murder per 100,000, age adjusted"
life_murder_conf = get_config(data, X_AXIS, Y_AXIS)
year = life_murder_conf["years"][-1]

plotly.offline.iplot(
    {
        "data": [
            go.Scatter(
                x=life_murder_conf["x_df"][year],
                y=life_murder_conf["y_df"][year],
                mode="markers",
                marker={"size": 10},
            )
        ],
        "layout": {
            "title": f"Year {year}",
            "xaxis": {"title": X_AXIS},
            "yaxis": {"title": Y_AXIS},
        },
    }
)
