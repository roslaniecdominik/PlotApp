import numpy as np
import pandas as pd

def calc_statistics(data, selected_datas, filepath):
    try:
        dict = {
            "Satellite Vehicle": ["nG", "nE", "nR", "nC", "nJ", "nGNSS"],
            "DOP factors": ["PDop", "TDop", "HDop", "VDop", "GDop"],
            "Receiver Clock Estimation": ["RecClkG", "RecClkR", "RecClkE", "RecClkC", "RecClkJ", "RecClkS"],
            "REC dNEU": ["RecN", "RecE", "RecU"],
            "REC mNEU": ["RecmN", "RecmE", "RecmU"],
            "Zenith Tropospheric Delay" : ["ZTD"],
            "REC XYZ": ["RecX", "RecY", "RecZ"],
            "REC NEU": ["RecN", "RecE", "RecU"]
        }
        stat_list = []
        for selected_data in selected_datas:
            data_listnames = [col for col in dict[selected_data] if col in data.columns] #check if they are in data            
            data_listnames = [col for col in data_listnames if not (data[col].isna().all() or (data[col].fillna(0) == 0).all())] #removes if 0/NaN in all
            
            if selected_data == "Satellite Vehicle" or selected_data == "DOP factors":

                mean_values = [data[data_listname].mean() for data_listname in data_listnames]
                min_values = [data[data_listname].min() for data_listname in data_listnames]
                max_values = [data[data_listname].max() for data_listname in data_listnames]
                stat_text_list = []
                stat_text_list.append(f"max: {' '.join([f'{col}:{mean_values[i]:.2f}' for i, col in enumerate(data_listnames)])}")
                stat_text_list.append(f"min: {' '.join([f"{col}:{min_values[i]:.2f}" for i, col in enumerate(data_listnames)])}")
                stat_text_list.append(f"max: {' '.join([f"{col}:{max_values[i]:.2f}" for i, col in enumerate(data_listnames)])}")
                
                stat_text = "\n".join(stat_text_list)
                stat_list.append(stat_text)
            
            if selected_data == "Receiver Clock Estimation" or selected_data == "REC mNEU" or selected_data == "Zenith Tropospheric Delay":
                
                data_listnames = [col for col in data_listnames if not (data[col].isna().all() or (data[col].fillna(0) == 0).all())] #removes if 0/NaN in all
                stat_text_list = []
                for element in data_listnames:
                    stat_text_list.append(f"{element}: \u03BC = {data[element].mean():.3f}   \u03C3 = {np.std(data[element]):.3f}")
                stat_text = "\n".join(stat_text_list)
                stat_list.append(stat_text)
                
            if selected_data == "REC dNEU" or selected_data == "REC NEU" or selected_data == "REC XYZ":
                inf_filepath = list(filter(lambda x: "Inf" in x, filepath))
                if inf_filepath:
                    inf_data = pd.read_csv(inf_filepath[0], sep=';', index_col=False, skipinitialspace=True)

                    if selected_data == "REC XYZ":
                        ref_list = ["RefX", "RefY", "RefZ"]
                    else:
                        ref_list = ["RefN", "RefE", "RefU"]

                    stat_text_list = []

                    for element, ref in zip(data_listnames, ref_list):
                        stat_text_list.append(f"{element}: \u03BC = {(data[element].mean() - inf_data[ref].mean()):.3f}   \u03C3 = {np.std(data[element]):.3f}")
                    if selected_data == "REC XYZ" or selected_data == "REC NEU":
                        stat_list.extend([i for i in stat_text_list])
                    else:  
                        stat_text = "\n".join(stat_text_list)
                        stat_list.append(stat_text)
    except:
        stat_list = []
    return stat_list