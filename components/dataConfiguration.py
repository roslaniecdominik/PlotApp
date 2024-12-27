import pandas as pd
import numpy as np
import colorsys

def generate_shades(data_list, saturation=0.85): 
    # base_hue: 0.0 - red; 0.33 - green, 0.67 - blue
    #           0.17 - yellow; 0.5 - cyan; 0.83 - magenta
    
    solutions = list(set(item.split()[-1] for item in data_list))
    
    base_hue = [0.33, 0.58, 0.0, 0.9, 0.17, 0.45]
    colors = []

    for i, solution in enumerate(solutions): 
        count = sum(1 for item in data_list if solution in item.split())
        for j in range(count):
            lightness = 0.6 + (j- count / 2) * 0.3 / count

            r, g, b = colorsys.hls_to_rgb(base_hue[i], lightness, saturation)
                
            color = (int(r*225), int(g*225), int(b*225))
                
            colors.append("#{:02x}{:02x}{:02x}".format(*color))
    return colors

def data_solution_generator(solutions, list_data):
    solutions_list = [_.strip() for _ in solutions.split(",")]
    data_listname = []
    if "PRN" in list_data:
        for solution in solutions_list:
            for element in list_data:
                data_listname.append(f"{element}_{solution}")
    else:
        for solution in solutions_list:
            for element in list_data:
                data_listname.append(f"{element} {solution}")
    return data_listname

def datasets_dict():
    data_sets_dict = {
        "Est set": ["DOP factors", "REC dNEU", "REC mNEU", "Receiver Clock Estimation", "Satellite Vehicle", "Zenith Tropospheric Delay"],
        "Amb set": ["m Phase Ambiguity", "Phase Ambiguity"],
        "QC set": ["Code Residuals", "Phase Residuals", "PRN"],
        "XYZ set": ["REC XYZ", "REC mXYZ"],
        "NEU set": ["REC NEU", "REC mNEU"]
    }
    return data_sets_dict

def defining_data():
    
    data_dict = {
        "PDop": "DOP factors", 
        "RecX": "REC XYZ", 
        "RecmX": "REC mXYZ",
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
    single_plot = ["DOP factors", "Ionospheric delay", "Satellite Vehicle", "REC mNEU", "REC mXYZ", "REC dNEU", "Zenith Tropospheric Delay", "Receiver Clock Estimation"]
    triple_plot = ["REC XYZ", "RecX", "RecY", "RecZ", "REC NEU", "RecN", "RecE", "RecU"]
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
            case "REC mXYZ":
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
                data_listname.append(["PRN", "Typ", "AvailablePRNs"])
    return data_listname

def match_data_after(data, solutions):
    data_listname = []

    for i in data:
        match i:
            case "DOP factors":
                data_listname.append(["PDop", "TDop", "HDop", "VDop", "GDop"])
            case "Satellite Vehicle":
                data_listname.append(["nGNSS", "nG", "nE", "nR", "nC", "nJ"])
            case "REC XYZ":
                data_listname.append(["RecX", "RecY", "RecZ"])
            case "REC mXYZ":
                data_listname.append(["RecmX", "RecmY", "RecmZ"])
            case "Ionospheric delay":
                data_listname.append(["mIonDel"])
            case "REC NEU":
                data_listname.append(["RecN", "RecE", "RecU"])
            case "REC dNEU":
                data_listname.append(["RecdN", "RecdE", "RecdU"])
            case "REC mNEU":
                data_listname.append(["RecmN", "RecmE", "RecmU"])
            case "Phase Ambiguity":
                list_data = ["N_IF", "N_L1", "N_L2", "N_L3", "N_L4", "N_L5", "N_L6", "N_L7", "N_L8"]
                data_listname.append(data_solution_generator(solutions, list_data))
            case "m Phase Ambiguity":
                list_data = ["mN_L1", "mN_L2", "mN_L3", "mN_L4", "mN_L5", "mN_L6", "mN_L7", "mN_L8"]
                data_listname.append(data_solution_generator(solutions, list_data))
            case "Zenith Tropospheric Delay":
                data_listname.append(["mZTD+", "mZTD-", "ZTD", "ExZTD"])
            case "Receiver Clock Estimation":
                data_listname.append(["RecClkG", "RecClkR", "RecClkE", "RecClkC", "RecClkJ", "RecClkS"])
            case "Code Residuals":
                list_data = ["C_Res1", "C_Res2", "C_Res3", "C_Res4", "C_Res5", "C_Res6", "C_Res7", "C_Res8", "C_Res_IF"]
                data_listname.append(data_solution_generator(solutions, list_data))
            case "Phase Residuals":
                list_data = ["L_Res1", "L_Res2", "L_Res3", "L_Res4", "L_Res5", "L_Res6", "L_Res7", "L_Res8", "L_Res_IF"]
                data_listname.append(data_solution_generator(solutions, list_data))
            case "PRN":
                list_data = ["PRN"]
                prn_solution_list = data_solution_generator(solutions, list_data)
                prn_list = ["AvailablePRNs", "Bad IFree", "No Clock", "No Orbit", "Cycle Slips", "Outliers", "Eclipsing"]
                data_listname.append(prn_list[:1] + prn_solution_list + prn_list[1:])

    return data_listname

def match_color(data, data_listnames):
    data_colors = []
    for i, data_listname in zip(data, data_listnames):
        match i:
            case "DOP factors":
                data_colors.append(["red", "green", "blue", "yellow", "orange"])
            case "Satellite Vehicle":
                data_colors.append(["black", "limegreen", "dodgerblue", "red", "orange", "yellow"])
            case "REC XYZ":
                data_colors.append(["red"])
                data_colors.append(["green"])
                data_colors.append(["blue"])
            case "REC mXYZ":
                data_colors.append(["red", "green", "blue"])
            case "Ionospheric delay":
                data_colors.append(["red"])
            case "REC NEU":
                data_colors.append(["red"])
                data_colors.append(["green"])
                data_colors.append(["blue"])
            case "REC dNEU":
                data_colors.append(["red", "green", "blue"])
            case "REC mNEU":
                data_colors.append(["green", "blue", "red"])
            case "Phase Ambiguity":
                data_colors.append(generate_shades(data_listname))
            case "m Phase Ambiguity":
                data_colors.append(generate_shades(data_listname))
            case "Zenith Tropospheric Delay":
                data_colors.append(["mistyrose", "mistyrose", "red", "brown"])
            case "Receiver Clock Estimation":
                data_colors.append(["limegreen", "dodgerblue", "red", "black", "orange", "blue"])
            case "Code Residuals":
                data_colors.append(generate_shades(data_listname))
            case "Phase Residuals":
                data_colors.append(generate_shades(data_listname))
            case "PRN":
                color_list = []
                for layer in data_listname:
                    match layer:
                        case "AvailablePRNs":
                            color_list.append("black")
                        case "PRN_GPS":
                            color_list.append("limegreen")
                        case "PRN_GALILEO":
                            color_list.append("dodgerblue")
                        case "Bad IFree":
                            color_list.append("pink")
                        case "No Clock":
                            color_list.append("orange")
                        case "No Orbit":
                            color_list.append("green")
                        case "Cycle Slips":
                            color_list.append("blue")
                        case "Outliers":
                            color_list.append("red")
                        case "Eclipsing":
                            color_list.append("grey")

                data_colors.append(color_list)

    return data_colors

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
            data = data.drop_duplicates()


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

            elif len(data) > len(data_last) and any("PRN" in col for col in data_last.columns):
                data_last = data_last.drop(columns=[col for col in data.columns if col in data_last.columns and col != 'datetime'])
                pd.set_option('display.max_columns', None)
                
                data["row_number"] = data.groupby("datetime").cumcount()
                data_last["row_number"] = data_last.groupby("datetime").cumcount()                
                data = pd.merge(data, data_last, on=['datetime', 'row_number'], how='left')

            else: #if data_last has longer PRN than data
                data = data.set_index('datetime')
                data_last = data_last.set_index('datetime')
                data = data.combine_first(data_last).reset_index()
    
    if selected_data == "PRN": #Available PRNs converter
        def transform_numbers_column(df):
            new_numbers_column = []

            for time_value, group in df.groupby('datetime'):
                repeat_count = len(group)
                new_numbers_column.append(' '.join(group.iloc[0]['AvailablePRNs'].split()))

                for _ in range(repeat_count - 1):
                    new_numbers_column.append('NaN')

            df['AvailablePRNs'] = pd.Series(new_numbers_column)
            return df
        data = transform_numbers_column(data)


    return data


def data_filtering(data, data_listnames):

    for j in range(len(data_listnames)):

        index_to_del = [i for i, col in enumerate(data_listnames[j]) if data[col].replace(0, np.nan).isna().all()]
        columns_to_del = [data_listnames[j][i] for i in index_to_del]

        data = data.drop(columns=columns_to_del)
        
        for i in sorted(index_to_del, reverse=True): del data_listnames[j][i]
        # for i in sorted(index_to_del, reverse=True): del data_colors[j][i]
        data = data.replace(0, np.nan)
    return data, data_listnames
    
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
    
    for i in range(len(selected_datas)):
        if selected_datas[i] in triple_plot:
            for j in range(len(data_listnames[i])):
                new_listname.append([data_listnames[i][j]])
                # new_listcolors.append([data_colors[i][j]])
        else:
            new_listname.append(data_listnames[i])
            # new_listcolors.append(data_colors[i])

    for el in triple_plot:
        if el in selected_datas:
            index = selected_datas.index(el)

            if selected_datas[index] == "REC XYZ":
                selected_datas[index] = "RecZ"
                selected_datas.insert(index, "RecY")
                selected_datas.insert(index, "RecX")
            elif selected_datas[index] == "REC NEU":
                selected_datas[index] = "RecU"
                selected_datas.insert(index, "RecE")
                selected_datas.insert(index, "RecN")
    # new_listcolors = [['springgreen', 'limegreen', 'deepskyblue', 'dodgerblue']]
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
    
def transform_numbers_column(data):
    result = (
        data.dropna(subset=['AvailablePRNs'])
        .groupby('datetime')['AvailablePRNs']
        .first()
        .reset_index()
    )
    
    expanded_rows = []
    
    for _, row in result.iterrows():
        for num in list(map(int, row['AvailablePRNs'].split())):
            expanded_rows.append({'datetime': row['datetime'], 'AvailablePRNs': num})
    expanded_df = pd.DataFrame(expanded_rows)
    
    return expanded_df