import customtkinter as ctk

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

        for point, var in checkbox_states.items():
            if not var.get() and selected_points + value_to_add_dict[point] > max_points:
                checkboxes[point].configure(state="disabled")
            else:
                checkboxes[point].configure(state="normal")

    menu_window = ctk.CTkToplevel(app)
    menu_window.title("Options")
    menu_height = (len(value_to_add)+1) * 30 + 60
    menu_window.geometry(f"200x{menu_height}")

    checkboxes = {}
    for option, points in value_to_add_dict.items():
        var = ctk.BooleanVar()
        checkbox_states[option] = var
        checkbox = ctk.CTkCheckBox(menu_window, text=option, variable=var, command=on_checbox_change)
        checkbox.pack(anchor="w", padx=10, pady=5)
        checkboxes[option] = checkbox

    def save_selection():
        
        selected_data = [option for option, var in checkbox_states.items() if var.get()]
        if on_selections_change:
            on_selections_change(selected_data)
        # read_time_in_thread("")
        menu_window.destroy()
        data_menu.set("...")

    close_button = ctk.CTkButton(menu_window, text="Save", command=save_selection)
    close_button.pack(pady=10)