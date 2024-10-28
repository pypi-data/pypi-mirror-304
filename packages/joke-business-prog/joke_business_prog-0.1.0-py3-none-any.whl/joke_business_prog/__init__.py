def clear_profit(revenue, costs):
    return float(revenue) - float(costs)

def roi(revenue, costs):
    return (float(revenue) / float(costs)) * 100

__all__ = ['clear_profit', 'roi']