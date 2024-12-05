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
    return data