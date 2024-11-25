def xaxis_config (time_diff, timedelta):
    if (time_diff > timedelta(days=365*2)):
        xaxis_set = "%y"
        xaxis_label = "TIME [year]"
    elif (time_diff <= timedelta(days=365*2)) and (time_diff > timedelta(days=6*31)):
        xaxis_set = "%y-%m"
        xaxis_label = "TIME [year-month]"
    elif (time_diff <= timedelta(days=6*31)) and (time_diff > timedelta(days=2*31)):
        xaxis_set = "%m-%d"
        xaxis_label = "TIME [month-day]"
    elif (time_diff <= timedelta(days=2*31)) and (time_diff > timedelta(days=31)):
        xaxis_set = "%m-%d %H"
        xaxis_label = "TIME [month-day hour]"
    elif (time_diff <= timedelta(days=31)) and (time_diff > timedelta(days=1)):
        xaxis_set = "%d %H:%M"
        xaxis_label = "TIME [day hour:min]"
    elif (time_diff <= timedelta(hours=24)) and (time_diff > timedelta(hours=1)):
        xaxis_set = "%H:%M"
        xaxis_label = "TIME [hour:min]"
    elif time_diff < timedelta(minutes=60):
        xaxis_set = "%M:%S"
        xaxis_label = "TIME [min:sec]"
    else:
        xaxis_set = "%Y-%m-%d %H:%M"
        xaxis_label = "TIME [year-month-day hour:min]"
    return xaxis_set, xaxis_label
        
        