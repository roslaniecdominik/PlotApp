import re
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

def yaxis_label(selected_data):
    m_list = ["RECm XYZ", "REC dNEU", "REC mNEU", "Zenith Tropospheric Delay", "Receiver Clock Estimation", "Code Residuals", "Phase Residuals", "Ionospheric delay"]
    cycles_list = ["Phase Ambiguity", "m Phase Ambiguity"]

    # selected_data = re.sub(r" (?!.* )", "\n", selected_data)
    if selected_data in m_list:
        selected_data_unit = ((re.sub(r" (?!.* )", "\n", selected_data)) + " [m]")
    elif selected_data in cycles_list:
        if selected_data == "m Phase Ambiguity":
            selected_data_unit = "\u03C3 of Phase Ambiguity [cycles]"
        else:
            selected_data_unit = ((re.sub(r" (?!.* )", "\n", selected_data)) + " [cycles]")
        
    elif selected_data in ["Rec X", "Rec Y", "Rec Z", "Rec N", "Rec E", "Rec U"]:
        selected_data_unit = selected_data + " [m]"
    else:
        selected_data_unit = ((re.sub(r" (?!.* )", "\n", selected_data)))

    return selected_data_unit
