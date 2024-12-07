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
                "RecClkG": "Receiver Clock Estimation",
                "C_Res1": "Code Residuals",
                "L_Res1": "Phase Residuals",
                ";PRN": "PRN"}
    single_scatter = ["Phase Ambiguity", "Code Residuals", "Phase Residuals", "PRN"]
    single_plot = ["DOP factors", "Ionospheric delay", "Satellite Vehicle", "REC mNEU", "RECm XYZ", "REC dNEU", "Zenith Tropospheric Delay", "Receiver Clock Estimation"]
    triple_plot = ["REC XYZ", "REC NEU"]
    return data_dict, single_scatter, single_plot, triple_plot

def match_data_before(data):
    data_listname = []
    for i in data:
        match i:
            case "DOP factors":
                data_listname.append(["PDop", "TDop", "HDop", "VDop", "GDop"])
            case "Satellite Vehicle":
                data_listname.append(["nG", "nE", "nR", "nC", "nJ"])
            case "REC XYZ":
                data_listname.append(["RecX", "RecY", "RecZ"])
            case "RECm XYZ":
                data_listname.append(["RecmX", "RecmY", "RecmZ"])
            case "Ionospheric delay":
                data_listname.append(["mIonDel"])
            case "REC NEU":
                data_listname.append(["RecN", "RecE", "RecU"])
            case "REC dNEU":
                data_listname.append(["RecN", "RecE", "RecU"])
            case "REC mNEU":
                data_listname.append(["RecmN", "RecmE", "RecmU"])
            case "Phase Ambiguity":
                data_listname.append(["N_IF", "N_L1", "N_L2", "N_L3", "N_L4", "N_L5", "N_L6", "N_L7", "N_L8", "PRN"])
            case "Zenith Tropospheric Delay":
                data_listname.append(["ZTD", "mZTD"])
            case "Receiver Clock Estimation":
                data_listname.append(["RecClkG", "RecClkR", "RecClkE", "RecClkC", "RecClkJ", "RecClkS"])
            case "Code Residuals":
                data_listname.append(["C_Res1", "C_Res2", "C_Res3", "C_Res4", "C_Res5", "C_Res6", "C_Res7", "C_Res8", "C_Res_IF"])
            case "Phase Residuals":
                data_listname.append(["L_Res1", "L_Res2", "L_Res3", "L_Res4", "L_Res5", "L_Res6", "L_Res7", "L_Res8", "L_Res_IF"])
            case "PRN":
                data_listname.append(["PRN", "Typ"])
        return data_listname

def match_data_after(data):
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
                data_listname.append(["N_IF GPS", "N_L1 GPS", "N_L2 GPS", "N_L3 GPS", "N_L4 GPS", "N_L5 GPS", "N_L6 GPS", "N_L7 GPS", "N_L8 GPS",
                                      "N_IF Galileo", "N_L1 Galileo", "N_L2 Galileo", "N_L3 Galileo", "N_L4 Galileo", "N_L5 Galileo", "N_L6 Galileo", "N_L7 Galileo", "N_L8 Galileo"])
                data_colors.append(["limegreen"]*9 + ["dodgerblue"]*9)
            case "Zenith Tropospheric Delay":
                data_listname.append(["mZTD+", "mZTD-", "ZTD", "ExZTD"])
                data_colors.append(["mistyrose", "mistyrose", "red", "brown"])
            case "Receiver Clock Estimation":
                data_listname.append(["RecClkG", "RecClkR", "RecClkE", "RecClkC", "RecClkJ", "RecClkS"])
                data_colors.append(["green", "blue", "red", "black", "orange", "aqua"])
            case "Code Residuals":
                data_listname.append(["C_Res1", "C_Res2", "C_Res3", "C_Res4", "C_Res5", "C_Res6", "C_Res7", "C_Res8", "C_Res_IF"])
                data_colors.append(["green", "blue", "red", "blue", "red", "blue", "green", "blue", "green"])
            case "Phase Residuals":
                data_listname.append(["L_Res1", "L_Res2", "L_Res3", "L_Res4", "L_Res5", "L_Res6", "L_Res7", "L_Res8", "L_Res_IF"])
                data_colors.append(["green", "blue", "red", "blue", "red", "blue", "green", "blue", "green"])
            case "PRN":
                data_listname.append(["PRN_GPS", "PRN_Galileo", "Bad IFree", "No Clock", "No Orbit", "Cycle Slips", "Outliers", "Eclipsing"])
                data_colors.append(["limegreen", "dodgerblue", "pink", "orange", "limegreen", "dodgerblue", "red", "grey"])

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
    data_listnames = match_data_before(selected_data)

    existing_columns = [col for col in data_listnames if all(c in data.columns for c in col)]
    missing_columns = [col for col in data_listnames if not all(c in data.columns for c in col)]

    if len(filepath) >= 2: #2 bo narazie zdefiniowane ploty opierają się o maks 2 pliki
        data_last = pd.read_csv(filepath[1], sep=';', index_col=False, skipinitialspace=True)
        data_last = time_column(data_last)

        if "Err" in filepath[1]: #zestaw
            data_last = data_last.rename(columns={'PRN': 'PRN_sign'})

        if data_last['datetime'].isin(data['datetime']).any() and len(missing_columns) == 0: #ten sam dzień
            data = pd.concat([data, data_last], axis=1)

        elif len(missing_columns) != 0 and "PRN" in selected_data:

            data = pd.merge(data_last, data, on='datetime', how='outer')
            for col in data.columns:
                if '_x' in col:
                    base_col = col.split('_x')[0]
                    if f"{base_col}_y" in data.columns:
                        data[base_col] = data[col].combine_first(data[f"{base_col}_y"])
                        data = data.drop(columns=[col, f"{base_col}_y"])

        elif len(missing_columns) != 0: #dane z innego pliku (phase)
            data = pd.merge(data, data_last, on='datetime', how='outer')



        elif len(existing_columns) != 0: #dane z tych samych plików z różnych dni
            data = pd.concat([data, data_last], ignore_index=True)


    
    if len(filepath) > 2:

        for i in range(len(filepath)-2):

            data_last = pd.read_csv(filepath[i+2], sep=';', index_col=False, skipinitialspace=True)
            data_last = time_column(data_last)

            if "Err" in filepath[i+2]: #zestaw
                data_last = data_last.rename(columns={'PRN': 'PRN_sign'})

            if filepath[i+2][filepath[i+2].rfind("_") +1:filepath[i+2].rfind(".")] == filepath[0][filepath[0].rfind("_") +1:filepath[0].rfind(".")]:
                data = pd.concat([data, data_last], ignore_index=True)

            else:
                data = data.set_index('datetime')
                data_last = data_last.set_index('datetime')

                data = data.combine_first(data_last).reset_index()


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

def prn_filtering(filepath):
    found_err = False
    found_res = False
    found_avs = False

    for file in filepath:
        if "Err" in file:
            found_err = True
        if "Res" in file:
            found_res = True
        if "AvS" in file:
            found_avs = True
        if found_res and found_avs and found_err:
            break

    if not found_err and not found_res and not found_avs: 
        return True
    else:
        return found_res and found_avs and found_err