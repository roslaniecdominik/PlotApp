import numpy as np
def calculate_new_columns(data, selected_datas):
    for selected_data in selected_datas:
        if selected_data == "Satellite Vehicle":
            data["nGNSS"] = data["nE"] + data["nG"] + data["nR"] + data["nC"] + data["nJ"] + data["nS"]
        elif selected_data == "REC dNEU":
            data["RecdN"] = data["RecN"] - data["RecN"].mean()
            data["RecdE"] = data["RecE"] - data["RecE"].mean()
            data["RecdU"] = data["RecU"] - data["RecU"].mean()
        elif selected_data == "Zenith Tropospheric Delay":
            data["mZTD+"] = data["ZTD"] + data["mZTD"]
            data["mZTD-"] = data["ZTD"] - data["mZTD"]
        elif selected_data == "PRN":
            data["PRN_GPS"] = data["PRN"].apply(lambda x: x if x < 40 else np.nan)
            data["PRN_Galileo"] = data["PRN"].apply(lambda x: x if x > 40 else np.nan)
            data["Bad IFree"] = np.where(data["Typ"] == "BIF", data["PRN_sign"], np.nan)
            data["No Clock"] = np.where(data["Typ"] == "NCL", data["PRN_sign"], np.nan)
            data["No Orbit"] = np.where(data["Typ"] == "NOR", data["PRN_sign"], np.nan)
            data["Cycle Slips"] = np.where(data["Typ"] == "CSL", data["PRN_sign"], np.nan)
            data["Outliers"] = np.where(data["Typ"] == "OUT", data["PRN_sign"], np.nan)
            data["Eclipsing"] = np.where(data["Typ"] == "ECL", data["PRN_sign"], np.nan)
        elif selected_data == "Phase Ambiguity":
            list_GPS = ["N_IF GPS", "N_L1 GPS", "N_L2 GPS", "N_L3 GPS", "N_L4 GPS", "N_L5 GPS", "N_L6 GPS", "N_L7 GPS", "N_L8 GPS"]
            list_Galileo = ["N_IF Galileo", "N_L1 Galileo", "N_L2 Galileo", "N_L3 Galileo", "N_L4 Galileo", "N_L5 Galileo", "N_L6 Galileo", "N_L7 Galileo", "N_L8 Galileo"]
            for element in list_GPS:
                data[element] = np.where(data["PRN"] < 40, data[element.split()[0]], np.nan)
            for element in list_Galileo:
                data[element] = np.where(data["PRN"] > 40, data[element.split()[0]], np.nan)

    return data