import pandas as pd

def defining_data():
    
    data_dict = {"PDop": "DOP factors", 
                "RecX": "REC XYZ", 
                "RecmX": "RECm XYZ", 
                "mIonDel": "ION",
                "RecN": "NEU",
                "RecE": "dNEU",
                "RecmN": "mNEU",
                "nG": "SV",
                "N_L1": "phase"}
    single_scatter = ["phase"]
    single_plot = ["DOP factors", "ION", "SV", "mNEU", "RECm XYZ", "dNEU"]
    triple_plot = ["REC XYZ", "NEU"]
    return data_dict, single_scatter, single_plot, triple_plot


def match_data(data):
    match data:
        case "DOP factors":
            data_listname = ["PDop", "TDop", "HDop", "VDop", "GDop"]
            data_colors = ["red", "green", "blue", "yellow", "orange"]
        case "SV":
            data_listname = ["nG", "nE", "nR", "nC", "nJ", "nGNSS"]
            data_colors = ["red", "green", "blue", "yellow", "orange", "black"]
        case "REC XYZ":
            data_listname = ["RecX", "RecY", "RecZ"]
            data_colors = ["red", "green", "blue"]
        case "RECm XYZ":
            data_listname = ["RecmX", "RecmY", "RecmZ"]
            data_colors = ["red", "green", "blue"]
        case "ION":
            data_listname = ["mIonDel"]
            data_colors = ["red"]
        case "NEU":
            data_listname = ["RecN", "RecE", "RecU"]
            data_colors = ["red", "green", "blue"]
        case "dNEU":
            data_listname = ["RecdN", "RecdE", "RecdU"]
            data_colors = ["red", "green", "blue"]
        case "mNEU":
            data_listname = ["RecmN", "RecmE", "RecmU"]
            data_colors = ["green", "blue", "red"]
        case "phase":
            data_listname = ["N_L1", "N_L2", "N_L3", "N_L4", "N_L5", "N_L6", "N_L7", "N_L8"]
            data_colors = ["black", "grey", "rosybrown", "brown", "tomato", "orange", "olivedrab", "aqua", "dodgerblue"]
    return data_listname, data_colors

def time_column(data):
        # Removing empty characters
        data.columns = data.columns.str.strip() 
        # Time column
        data["ss"] = data["ss"].abs()
        data["datetime"] = pd.to_datetime(data["YY"].astype(str) + '-' + 
                                        data["MM"].astype(str) + '-' + 
                                        data["DD"].astype(str) + ' ' + 
                                        data["hh"].astype(str) + ':' + 
                                        data["mm"].astype(str) + ':' + 
                                        data["ss"].astype(str))
        data = data.drop('YY', axis=1)
        data = data.drop('MM', axis=1)
        data = data.drop('DD', axis=1)
        data = data.drop('hh', axis=1)
        data = data.drop('mm', axis=1)
        data = data.drop('ss', axis=1)
        return data

def merge_data(data, selected_data, filepath):
    data_listname, x = match_data(selected_data)
    
    if len(filepath) > 2:
        data_to_merge = data
        data_listname.append("datetime")
        data_to_merge = data_to_merge[data_listname]
        for i in range(len(filepath)-1):
            if i < (len(filepath)-1): 
                data = pd.read_csv(filepath[i+1], sep=';', index_col=False, skipinitialspace=True)
                data = time_column(data)
                data = data[data_listname]
                merged = pd.concat([data_to_merge, data])
                data_to_merge = merged
        data = merged


    elif len(filepath) == 2:
        data_last = pd.read_csv(filepath[-1], sep=';', index_col=False, skipinitialspace=True)
        data_last = time_column(data_last)
        merged = pd.concat([data_last, data])
       
        data = merged
    return data
