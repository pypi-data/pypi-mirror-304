def net_profit(revenue, costs):
    return revenue - costs
def roi(revenue, costs):
    profit = net_profit(revenue, costs)
    if costs == 0:
        return 0.0
    return (profit / costs) * 100