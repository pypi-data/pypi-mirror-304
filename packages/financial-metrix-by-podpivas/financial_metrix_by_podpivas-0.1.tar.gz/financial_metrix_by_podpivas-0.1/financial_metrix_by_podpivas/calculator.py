def calculate_net_profit (revenue, costs):
    '''Находит общую прибыль'''
    return revenue - costs

def calculate_roi(net_profit, costs):
    '''Находит ROI'''
    if costs == 0:
        return 0
    else:
        return (net_profit / costs) * 100

