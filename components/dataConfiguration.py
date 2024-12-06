import pandas as pd
import numpy as np

from components.calculateNewColumns import calculate_new_columns


def defining_data():
    
    data_dict = {"PDop": "DOP factors", 
                "RecX": "REC XYZ", 
                "RecmX": "RECm XYZ",
                "mIonDel": "Ionospheric delay",
                "RecN": "REC NEU",
                "RecE": "REC dNEU",
                "RecmN": "REC mNEU",
                "nG": "Satellite Vehicle",
                "N_L1": "Phase Ambiguity",
                "ZTD": "Zenith Tropospheric Delay",
                "RecClkG": "Receiver Clock Estimation"}
    single_scatter = ["Phase Ambiguity"]
    single_plot = ["DOP factors", "Ionospheric delay", "Satellite Vehicle", "REC mNEU", "RECm XYZ", "REC dNEU", "Zenith Tropospheric Delay", "Receiver Clock Estimation"]
    triple_plot = ["REC XYZ", "REC NEU"]
    return data_dict, single_scatter, single_plot, triple_plot


def match_data(data):
    data_listname = []
    data_colors = [] 
    for i in data:
        match i:
            case "DOP factors":
                data_listname.append(["PDop", "TDop", "HDop", "VDop", "GDop"])
                data_colors.append(["red", "green", "blue", "yellow", "orange"])
            case "Satellite Vehicle":
                data_listname.append(["nG", "nE", "nR", "nC", "nJ", "nGNSS"])
                data_colors.append(["red", "green", "blue", "yellow", "orange", "black"])
            case "REC XYZ":
                data_listname.append(["RecX", "RecY", "RecZ"])
                data_colors.append(["red", "green", "blue"])
            case "RECm XYZ":
                data_listname.append(["RecmX", "RecmY", "RecmZ"])
                data_colors.append(["red", "green", "blue"])
            case "Ionospheric delay":
                data_listname.append(["mIonDel"])
                data_colors.append(["red"])
            case "REC NEU":
                data_listname.append(["RecN", "RecE", "RecU"])
                data_colors.append(["red", "green", "blue"])
            case "REC dNEU":
                data_listname.append(["RecdN", "RecdE", "RecdU"])
                data_colors.append(["red", "green", "blue"])
            case "REC mNEU":
                data_listname.append(["RecmN", "RecmE", "RecmU"])
                data_colors.append(["green", "blue", "red"])
            case "Phase Ambiguity":
                data_listname.append(["N_L1", "N_L2", "N_L3", "N_L4", "N_L5", "N_L6", "N_L7", "N_L8"])
                data_colors.append(["black", "grey", "rosybrown", "brown", "tomato", "orange", "olivedrab", "aqua", "dodgerblue"])
            case "Zenith Tropospheric Delay":
                data_listname.append(["mZTD+", "mZTD-", "ZTD", "ExZTD"])
                data_colors.append(["mistyrose", "mistyrose", "red", "brown"])
            case "Receiver Clock Estimation":
                data_listname.append(["RecClkG", "RecClkR", "RecClkE", "RecClkC", "RecClkJ", "RecClkS"])
                data_colors.append(["green", "blue", "red", "black", "orange", "aqua"])
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


def merge_data(data, selected_data, filepath, selected_station):
    data_listnames, _ = match_data(selected_data)

    def cuting_columns(dataframe, data_listname):
        cut_column = []
        [cut_column.extend(i) for i in data_listname]
        cut_column.insert(0, "datetime")

        cut_data = dataframe[cut_column]
        cut_data = cut_data.copy()
        cut_data.loc[:, "Sol"] = selected_station
        return cut_data

    existing_columns = [col for col in data_listnames if all(c in data.columns for c in col)]
    missing_columns = [col for col in data_listnames if not all(c in data.columns for c in col)]

    if len(filepath) >= 2: #2 bo narazie zdefiniowane ploty opierają się o maks 2 pliki
        data_last = pd.read_csv(filepath[1], sep=';', index_col=False, skipinitialspace=True)
        data_last = time_column(data_last)

        if data_last['datetime'].isin(data['datetime']).any() and len(missing_columns) == 0: #ten sam dzień
            data = pd.concat([data, data_last], ignore_index=True)
            data = calculate_new_columns(data, selected_data)


        elif len(missing_columns) != 0: #dane z innego pliku (phase)
            data = pd.merge(data, data_last, on='datetime', how='outer')

        elif len(existing_columns) != 0: #dane z tych samych plików z różnych dni
            data = pd.concat([data, data_last], ignore_index=True)


    
    if len(filepath) > 2:

        for i in range(len(filepath)-2):

            data_last = pd.read_csv(filepath[i+2], sep=';', index_col=False, skipinitialspace=True)
            data_last = time_column(data_last)

            if filepath[i+2][filepath[i+2].rfind("_") +1:filepath[i+2].rfind(".")] == filepath[0][filepath[0].rfind("_") +1:filepath[0].rfind(".")]:
                data = pd.concat([data, data_last], ignore_index=True)

            else:
                data = data.set_index('datetime')
                data_last = data_last.set_index('datetime')

                data = data.combine_first(data_last).reset_index()
    
    data = calculate_new_columns(data, selected_data)
    
    data = cuting_columns(data, data_listnames)
    
    return data


def data_filtering(data, data_listnames, data_colors):

    for j in range(len(data_listnames)):

        index_to_del = [i for i, col in enumerate(data_listnames[j]) if data[col].replace(0, np.nan).isna().all()]
        columns_to_del = [data_listnames[j][i] for i in index_to_del]

        data = data.drop(columns=columns_to_del)
        
        for i in sorted(index_to_del, reverse=True): del data_listnames[j][i]
        for i in sorted(index_to_del, reverse=True): del data_colors[j][i]
        data = data.replace(0, np.nan)
    return data, data_listnames, data_colors
    

def triple_plot_corrections(data_listnames, data_colors, selected_datas, triple_plot):
    new_listname = []
    new_listcolors = []
    from collections import Counter
    for i in range(len(selected_datas)):
        if selected_datas[i] in triple_plot:
            for j in range(len(data_listnames[i])):
                new_listname.append([data_listnames[i][j]])
                new_listcolors.append([data_colors[i][j]])
        else:
            new_listname.append(data_listnames[i])
            new_listcolors.append(data_colors[i])

    for el in triple_plot:
        if el in selected_datas:
            index = selected_datas.index(el)
            selected_datas.insert(index, el)
            selected_datas.insert(index, el)

    return new_listname, new_listcolors, selected_datas