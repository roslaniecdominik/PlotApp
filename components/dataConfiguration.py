import pandas as pd
import numpy as np

def datasets_dict():
    data_sets_dict = {
        "Est set": ["DOP factors", "REC dNEU", "REC mNEU", "Receiver Clock Estimation", "Satellite Vehicle", "Zenith Tropospheric Delay"],
        "Amb set": ["m Phase Ambiguity", "Phase Ambiguity"],
        "QC set": ["Code Residuals", "Phase Residuals", "PRN"],
        "XYZ set": ["REC XYZ", "RECm XYZ"],
        "NEU set": ["REC NEU", "REC mNEU"]
    }
    return data_sets_dict

def defining_data():
    
    data_dict = {
        "PDop": "DOP factors", 
        "RecX": "REC XYZ", 
        "RecmX": "RECm XYZ",
        "mIonDel": "Ionospheric delay",
        "RecN": "REC NEU",
        "RecE": "REC dNEU",
        "RecmN": "REC mNEU",
        "nG": "Satellite Vehicle",
        "N_L1": "Phase Ambiguity",
        "mN_L1": "m Phase Ambiguity",
        "ZTD": "Zenith Tropospheric Delay",
        "RecClkG": "Receiver Clock Estimation",
        "C_Res1": "Code Residuals",
        "L_Res1": "Phase Residuals",
        ";PRN": "PRN"
    }
    single_scatter = ["m Phase Ambiguity", "Phase Ambiguity", "Code Residuals", "Phase Residuals", "PRN"]
    single_plot = ["DOP factors", "Ionospheric delay", "Satellite Vehicle", "REC mNEU", "RECm XYZ", "REC dNEU", "Zenith Tropospheric Delay", "Receiver Clock Estimation"]
    triple_plot = ["REC XYZ", "Rec X", "Rec Y", "Rec Z", "REC NEU", "Rec N", "Rec E", "Rec U"]
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
            case "m Phase Ambiguity":
                data_listname.append(["mN_L1", "mN_L2", "mN_L3", "mN_L4", "mN_L5", "mN_L6", "mN_L7", "mN_L8", "PRN"])
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
            case "m Phase Ambiguity":
                data_listname.append(["mN_L1 GPS", "mN_L2 GPS", "mN_L3 GPS", "mN_L4 GPS", "mN_L5 GPS", "mN_L6 GPS", "mN_L7 GPS", "mN_L8 GPS",
                                      "mN_L1 Galileo", "mN_L2 Galileo", "mN_L3 Galileo", "mN_L4 Galileo", "mN_L5 Galileo", "mN_L6 Galileo", "mN_L7 Galileo", "mN_L8 Galileo"])
                data_colors.append(["limegreen"]*8 + ["dodgerblue"]*8)
            case "Zenith Tropospheric Delay":
                data_listname.append(["mZTD+", "mZTD-", "ZTD", "ExZTD"])
                data_colors.append(["mistyrose", "mistyrose", "red", "brown"])
            case "Receiver Clock Estimation":
                data_listname.append(["RecClkG", "RecClkR", "RecClkE", "RecClkC", "RecClkJ", "RecClkS"])
                data_colors.append(["green", "blue", "red", "black", "orange", "aqua"])
            case "Code Residuals":
                data_listname.append(["C_Res1 GPS", "C_Res2 GPS", "C_Res3 GPS", "C_Res4 GPS", "C_Res5 GPS", "C_Res6 GPS", "C_Res7 GPS", "C_Res8 GPS", "C_Res_IF GPS",
                                      "C_Res1 Galileo", "C_Res2 Galileo", "C_Res3 Galileo", "C_Res4 Galileo", "C_Res5 Galileo", "C_Res6 Galileo", "C_Res7 Galileo", "C_Res8 Galileo", "C_Res_IF Galileo"])
                data_colors.append(["limegreen"]*9 + ["dodgerblue"]*9)
            case "Phase Residuals":
                data_listname.append(["L_Res1 GPS", "L_Res2 GPS", "L_Res3 GPS", "L_Res4 GPS", "L_Res5 GPS", "L_Res6 GPS", "L_Res7 GPS", "L_Res8 GPS", "L_Res_IF GPS", 
                                      "L_Res1 Galileo", "L_Res2 Galileo", "L_Res3 Galileo", "L_Res4 Galileo", "L_Res5 Galileo", "L_Res6 Galileo", "L_Res7 Galileo", "L_Res8 Galileo", "L_Res_IF Galileo"])
                data_colors.append(["limegreen"]*9 + ["dodgerblue"]*9)
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

    if len(filepath) >= 2:
        data_last = pd.read_csv(filepath[1], sep=';', index_col=False, skipinitialspace=True)
        data_last = time_column(data_last)
        if "Err" in filepath[1]:
            data_last = data_last.rename(columns={'PRN': 'PRN_sign'})
            
        if "PRN" in data.columns and "PRN" in data_last.columns and data['PRN'].equals(data_last['PRN']): #if data_last has longer PRN than data
            data = data.set_index('datetime')
            data_last = data_last.set_index('datetime')
            data = data.combine_first(data_last).reset_index()

        elif (len(missing_columns) != 0 and "PRN" in selected_data and "Err" in filepath[1]): # if data has full PRN an data_last incompplete
            data["row_number"] = data.groupby("datetime").cumcount()
            data_last["row_number"] = data_last.groupby("datetime").cumcount()                
            data = pd.merge(data, data_last, on=['datetime', 'row_number'], how='left')

        elif len(missing_columns) != 0: #phase (2 files)
            data = pd.merge(data, data_last, on='datetime', how='outer')


        elif len(existing_columns) != 0: #same file but  from several days
            data = pd.concat([data, data_last], ignore_index=True)

    if len(filepath) > 2:
        
        for i in range(len(filepath)-2):

            data_last = pd.read_csv(filepath[i+2], sep=';', index_col=False, skipinitialspace=True)
            data_last = time_column(data_last)
            
            if "Err" in filepath[i+2]:
                data_last = data_last.rename(columns={'PRN': 'PRN_sign'})

            if filepath[i+2][filepath[i+2].rfind("_") +1:filepath[i+2].rfind(".")] == filepath[0][filepath[0].rfind("_") +1:filepath[0].rfind(".")]: #if same file from another day (Amb)
                data = pd.concat([data, data_last], ignore_index=True)

            elif len(data) > len(data_last) and "PRN" in data_last:
                data_last = data_last.drop(columns=[col for col in data.columns if col in data_last.columns and col != 'datetime'])
                data["row_number"] = data.groupby("datetime").cumcount()
                data_last["row_number"] = data_last.groupby("datetime").cumcount()                
                data = pd.merge(data, data_last, on=['datetime', 'row_number'], how='left')

            else: #if data_last has longer PRN than data
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
    
def cutting_columns(dataframe, data_listname, selected_solution):
    cut_column = []
    [cut_column.extend(i) for i in data_listname]
    cut_column.insert(0, "datetime")
    cut_data = dataframe[cut_column]
    cut_data = cut_data.copy()
    cut_data.loc[:, "Sol"] = selected_solution
    return cut_data

def cutting_rows(dataframe, data_listname):
    data_listname = [item for sublist in data_listname for item in sublist]
    data = dataframe.iloc[:dataframe[data_listname].notna().any(axis=1)[::-1].idxmax() + 1]

    return data

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

            if selected_datas[index] == "REC XYZ":
                selected_datas[index] = "Rec Z"
                selected_datas.insert(index, "Rec Y")
                selected_datas.insert(index, "Rec X")
            elif selected_datas[index] == "REC NEU":
                selected_datas[index] = "Rec U"
                selected_datas.insert(index, "Rec E")
                selected_datas.insert(index, "Rec N")

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