import customtkinter as ctk
from components.centerWindow import center_window

def open_options_window(on_selections_change=None, app=None, value_to_add=None, data_menu=None):
    points = {
        "DOP factors": 1, 
        "REC XYZ": 3, 
        "REC mXYZ": 1,
        "Ionospheric delay": 1,
        "REC NEU": 3,
        "REC dNEU": 1,
        "REC mNEU": 1,
        "Satellite Vehicle": 1,
        "Phase Ambiguity": 1,
        "m Phase Ambiguity": 1,
        "Zenith Tropospheric Delay": 1,
        "Receiver Clock Estimation": 1,
        "Code Residuals": 1,
        "Phase Residuals": 1,
        "PRN": 1
    }
    checkbox_states = {}
    max_points = 6

    value_to_add_dict = {}
    for value in value_to_add:
        if value in points:
            value_to_add_dict[value] = points[value]

    def on_checbox_change():

        selected_points = sum(value_to_add_dict[point] for point, var in checkbox_states.items() if var.get())

        if any(var.get() for var in checkbox_states.values()):
            close_button.configure(state="normal")
        else:
            close_button.configure(state="disabled")

        for point, var in checkbox_states.items():
            if not var.get() and selected_points + value_to_add_dict[point] > max_points:
                checkboxes[point].configure(state="disabled")
            else:
                checkboxes[point].configure(state="normal")

    menu_window = ctk.CTkToplevel(app)
    menu_window.title("Options")
    
    if len(value_to_add) > 13:
        var_frame = ctk.CTkScrollableFrame(menu_window, fg_color="transparent")
        height = 500
    else:
        var_frame = ctk.CTkFrame(menu_window, fg_color="transparent")
        height = 50 + 35*len(value_to_add)

    center_window(window=menu_window, width=250, height=height, info="customize")

    if len(value_to_add) != 0: var_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

    checkboxes = {}
    for option, points in value_to_add_dict.items():
        var = ctk.BooleanVar()
        checkbox_states[option] = var
        checkbox = ctk.CTkCheckBox(var_frame, text=option, variable=var, command=on_checbox_change)
        checkbox.pack(anchor="w", padx=10, pady=5)
        checkboxes[option] = checkbox

    def save_selection():
        
        selected_data = [option for option, var in checkbox_states.items() if var.get()]
        if on_selections_change:
            on_selections_change(selected_data)

        menu_window.destroy()
        data_menu.set("...")

    close_button = ctk.CTkButton(menu_window, text="Save", command=save_selection, state="disabled")
    close_button.pack(side=ctk.BOTTOM, pady=10)