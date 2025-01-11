import customtkinter as ctk
import threading
import pandas as pd
import numpy as np
import os
from datetime import datetime
from tkinter import filedialog, messagebox

from components.buttonState import buttonState
from components.centerWindow import center_window
from components.dataConfiguration import merge_data, time_column, defining_data, prn_filtering, match_data_after, cutting_columns, cutting_rows
from components.frames import minmax_frame, sliders_frame, selected_time
from plotCreator import create_plot
from components.sliderEvent import year_slider_event, hour_slider_event, time_updater
from components.timeLabelClearing import timeLabelClearing
from components.solutionGenerator import solution_generator
from components.calculateNewColumns import calculate_new_columns
from components.statistcs import calc_statistics
from components.dataConfiguration import datasets_dict
from components.choiceLimit import open_options_window

data_dict = defining_data()
color_index = 0

global selected_start_label_hour, selected_end_label_hour


def date_uploadig():
    if tabview.get() == "Start" and end_year_entry.get() == str(time_range[0]).split()[0]:
        start_year_entry.delete(0, ctk.END)
        start_year_entry.insert(0, end_year_entry.get())
    elif tabview.get() == "End" and start_year_entry.get() == str(time_range[-1]).split()[0]:
        end_year_entry.delete(0, ctk.END)
        end_year_entry.insert(0, start_year_entry.get())

def loading_animation():
    global color_index, loading_check
    colors = [("grey", "transparent", "transparent"), ("transparent", "grey", "transparent"), ("transparent", "transparent", "grey"), ("transparent", "grey", "transparent")]

    if loading_check:
        color_index = (color_index + 1) % len(colors)
        
        circle1.configure(fg_color=colors[color_index][0])
        circle2.configure(fg_color=colors[color_index][1])
        circle3.configure(fg_color=colors[color_index][2])
        app.after(333, loading_animation)

    else:
        circle1.configure(fg_color="transparent")
        circle2.configure(fg_color="transparent")
        circle3.configure(fg_color="transparent")

def create_plot_handler():
    global data_all_columns
    
    if "RecX" in selected_data:
        cord_index = selected_data.index("RecX")
        selected_data.remove("RecX")
        selected_data.remove("RecY")
        selected_data.remove("RecZ")
        selected_data.insert(cord_index, "REC XYZ")
    if "RecN" in selected_data:
        cord_index = selected_data.index("RecN")
        selected_data.remove("RecN")
        selected_data.remove("RecE")
        selected_data.remove("RecU")
        selected_data.insert(cord_index, "REC NEU")

    start_time = f"{start_year_entry.get()} {start_hour_entry.get()}"
    end_time = f"{end_year_entry.get()} {end_hour_entry.get()}"
    time_data = data_all_columns.loc[(data_all_columns['datetime'] >= start_time) & (data_all_columns['datetime'] <= end_time)]
    data_time = time_data.reset_index(drop=True)
    data_listnames = match_data_after(selected_data, selected_solution)

    data_time.replace([np.inf, -np.inf], np.nan, inplace=True)
    stat_list = calc_statistics(data_time, selected_data, filepaths_cut)

    data = cutting_columns(data_time, data_listnames, selected_solution_encoded)
    data = cutting_rows(data, data_listnames)    
    create_plot(start_time, end_time, filepaths, station_list, selected_station_solution, data, selected_data, app, stat_list, selected_solution)

def read_time():
    global data_all_columns, selected_data, filepath, loading_check, time_range, time_dif, selected_solution_encoded, stat_list

    show_plot_button.configure(state="disabled")

    filepath = []
    
    for filepath_cut in filepaths_cut:
        for key, value in data_dict.items():
            for selected in selected_data:
                if value == selected:
                    with open(filepath_cut, "r") as file:
                        first_row = file.readline()
                        if key in first_row:
                            if filepath_cut not in filepath:
                                if "Eztd" not in filepath_cut:
                                    filepath.append(filepath_cut)
                        elif value == "PRN" and "AvailablePRNs" in first_row:
                            filepath.append(filepath_cut)
                   
    if "Ionospheric delay" not in selected_data and any("IonDel" in _ for _ in filepath):
        filepath = [_ for _ in filepath if "IonDel" not in _]
    
    data_all_columns = pd.read_csv(filepath[0], sep=';', index_col=False, skipinitialspace=True)
    
    data_all_columns = time_column(data_all_columns)
  
    if "Err" in filepath[0]: #zestaw
        data_all_columns = data_all_columns.rename(columns={'PRN': 'PRN_sign'})

    data_all_columns = merge_data(data_all_columns, selected_data, filepath)
    if "Phase Ambiguity" in selected_data:
        def normalize_by_first_value(dataframe, group_col, value_cols):
            dataframe.columns = dataframe.columns.str.strip()
            df_out = dataframe.copy()
            for col in value_cols:
                df_out[col] = dataframe.groupby(group_col)[col].transform(lambda grp: grp - grp.iloc[0])
            return df_out
        data_all_columns = normalize_by_first_value(data_all_columns, "PRN", ["N_IF", "N_L1", "N_L2", "N_L3", "N_L4", "N_L5", "N_L6", "N_L7", "N_L8"])
    data_all_columns = calculate_new_columns(data_all_columns, selected_data, selected_solution, filepaths_cut)
    time_range = [datetime.strptime(str(min(data_all_columns["datetime"])), "%Y-%m-%d %H:%M:%S"), datetime.strptime(str(max(data_all_columns["datetime"])), "%Y-%m-%d %H:%M:%S")]

    time_dif = int((time_range[-1] - time_range[0]).days)

    min_label_value.configure(text=min(data_all_columns["datetime"]))
    max_label_value.configure(text=max(data_all_columns["datetime"]))
    

    time_updater(time_range[0], start_year_entry, start_hour_entry, start_year_slider, selected_start_label_year,  selected_start_label_hour, time_dif)
    start_minute = (datetime.strptime(time_range[0].strftime("%H:%M:%S"), "%H:%M:%S")).minute * 2
    start_hour_slider.configure(from_= start_minute, to=24*60*2-1, number_of_steps=24*60*2-1 - start_minute)

    time_updater(time_range[-1], end_year_entry, end_hour_entry, end_year_slider, selected_end_label_year, selected_end_label_hour, time_dif)
    end_minute = (datetime.strptime(time_range[-1].strftime("%H:%M:%S"), "%H:%M:%S")).minute * 2
    end_hour_slider.configure(from_=0, to=24*60*2-1-end_minute, number_of_steps=24*60*2-1 - end_minute)

    loading_check = False
    loading_animation()

    buttonState([show_plot_button, start_hour_slider, end_hour_slider])
    
    if time_dif != 0:
        buttonState([start_year_slider, end_year_slider])

def read_time_in_thread(event):
    global loading_check
    loading_check = True
    app.after(500, loading_animation)
    threading.Thread(target=read_time).start()

def select_set_fun(choice):
    global selected_data

    selected_data_sets = [choice]
    data_sets_dict = datasets_dict()
    selected_data = [item for key in selected_data_sets if key in data_sets_dict for item in data_sets_dict[key]]

    read_time_in_thread("")

def display_select_options(selected_options):
    global selected_data
    selected_data = selected_options
    read_time_in_thread("")
  
def read_data(event):
    global data_dict, loading_check, filepaths_cut, selected_station_solution, value_to_add, selected_solution, selected_solution_encoded

    show_plot_button.configure(state="disabled")

    selected_station_solution = station_menu_fullVAR.get()
    selected_station = selected_station_solution.split(" ")[0]
    selected_solution = selected_station_solution.split("(")[1].split(")")[0]
    selected_solution_encoded = solution_generator(selected_solution)

    filepaths_cut = [filepath for filepath in filepaths if selected_station in filepath and selected_solution_encoded in filepath]

    
    data_dict, single_scatter, single_plot, triple_plot = defining_data()

    various_data = []
    for filepath in filepaths_cut:
        with open(filepath, "r") as file:
            first_row = file.readline()
            for i in data_dict:
                if i in first_row:
                    if i not in various_data:
                        various_data.append(i)

    value_to_add = []
    for key, value in data_dict.items():
        if key in various_data:
            value_to_add.append(value)
    

    if not prn_filtering(filepaths_cut):
        value_to_add.remove("PRN")


    value_to_add = sorted(value_to_add, key=str.casefold)

    data_sets_dict = datasets_dict()
    data_sets = [key for key, values in data_sets_dict.items() if all(item in value_to_add for item in values)]
    data_menu.configure(values=data_sets)

    optionmenu_var = ctk.StringVar(value="Data..")
    data_menu.configure(variable=optionmenu_var)


    loading_check = False
    loading_animation()

    timeLabelClearing(*time_label_list)
    buttonState([data_menu, configure_data_button])

def read_data_in_thread(event):
    global loading_check

    def shorten_label(text, max_length=14):
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text

    station_fullLabel.configure(text=event) 
    station_menu_fullVAR.set(event)
    station_menu.set(shorten_label(event))

    loading_check = True
    app.after(500, loading_animation)
    threading.Thread(target=read_data, args=(event,)).start()

def read_station():
    global loading_check, station_list

    if filepaths:
        filename_entry.delete(0, ctk.END)
        filename_entry.insert(ctk.END, filepaths[0])

    optionmenu_var = ctk.StringVar(value="...")

    data_menu.configure(variable=optionmenu_var)
    station_menu.configure(variable=optionmenu_var)

    
    def station_finder(filepaths):
        station_list = []
        try:
            for i in range(len(filepaths)):
                filepath = filepaths[i]
                slash_id = filepath.rfind("/")
                reduced_filepath = filepath[slash_id+1:]
                _id = reduced_filepath.find("_")
                station = reduced_filepath[:_id]
                from re import search
                find_solution = search(r'_(\d{6})_', filepaths[i])

                if find_solution:
                    result = find_solution.group(1)
                    station += f" ({solution_generator(result)})"

                if station not in station_list:
                    station_list.append(station)

        except:
            messagebox.showinfo("WRONG FILE NAME")

        show_plot_button.configure(state="disabled")
        return(station_list)
    

    if filepaths != "":
        station_list = station_finder(filepaths)
        station_menu.configure(values=station_list)

        optionmenu_var = ctk.StringVar(value="Station..")
        station_menu.configure(variable=optionmenu_var)


    timeLabelClearing(*time_label_list)

    buttonState([station_menu])

    loading_check = False
    loading_animation()

def open_file(statement):
    global filepaths, loading_check
    
    if statement == "file":
        filepaths = filedialog.askopenfilenames(filetypes=[("Text files", "*.log")])

    elif statement == "folder":
        folder_paths = filedialog.askdirectory(title="Select folder")
        filepaths = ""
        if folder_paths:
            filepaths = []
            for item in os.listdir(folder_paths):
                filepaths.append(f"{folder_paths}/{item}")
            filepaths = tuple(filepaths)


    if len(filepaths) > 0:
        loading_check = True
        loading_animation()
        loading_station = threading.Thread(target=read_station)
        loading_station.start()
        show_plot_button.configure(state="disabled")
        configure_data_button.configure(state="disabled")
        data_menu.configure(state="disabled")
    else:
        station_menu.configure(state="disabled")



# -Main window-
ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()
app.title("PlotApp")

center_window(window=app, width=700, height=500)

# -File section-
file_section = ctk.CTkFrame(app, fg_color="transparent")
file_section.pack(side=ctk.TOP, fill=ctk.BOTH, padx=55, pady=10)
open_file_button = ctk.CTkButton(file_section, text="Upload file", width=90, bg_color="transparent", command=lambda: open_file("file"))
open_file_button.pack(side=ctk.LEFT, fill=ctk.BOTH)
open_catalog_button = ctk.CTkButton(file_section, text="Upload folder", width=90, bg_color="transparent", command=lambda: open_file("folder"))
open_catalog_button.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=(10,0))
filename_entry = ctk.CTkEntry(file_section, border_width=0)
filename_entry.pack(side=ctk.RIGHT, fill=ctk.BOTH, padx=(10,0), expand=True)

# -Station & data section-
station_fullLabel = ctk.CTkLabel(app, text=" ", font=("Helvetica", 12))
station_fullLabel.pack(side=ctk.TOP)

stationData_section = ctk.CTkFrame(app, border_width=0, fg_color="transparent")
stationData_section.pack(side=ctk.TOP, fill=ctk.X, padx=55, pady=(5,5))
stationData_section.grid_columnconfigure((0, 1, 2), weight=1)

station_section = ctk.CTkFrame(stationData_section, border_width=0, fg_color="transparent")
station_section.grid(row=0, column=0, padx=10, sticky="ew")

station_label = ctk.CTkLabel(station_section, text="Select station", font=("Helvetica", 16))
station_label.pack(side=ctk.TOP, padx=(0,10))


station_menu_fullVAR = ctk.StringVar(station_section)
station_menu_variable = ctk.StringVar(value="...")
station_menu = ctk.CTkOptionMenu(station_section, width=150, values=[], variable=station_menu_variable, state="disabled", command=read_data_in_thread)
station_menu.pack(side=ctk.TOP)


data_section = ctk.CTkFrame(stationData_section, border_width=0, fg_color="transparent")
data_section.grid(row=0, column=1, padx=10, sticky="ew")

data_label = ctk.CTkLabel(data_section, text="Select data set", font=("Helvetica", 16))
data_label.pack(side=ctk.TOP, padx=(0,10))

data_menu_variable = ctk.StringVar(value="...")
data_menu = ctk.CTkOptionMenu(data_section, width=150, values=[], variable=data_menu_variable, state="disabled", command=select_set_fun)
data_menu.pack(side=ctk.TOP)


configure_data_section = ctk.CTkFrame(stationData_section, border_width=0, corner_radius=10, fg_color="transparent")
configure_data_section.grid(row=0, column=2, padx=10, sticky="ew")

configure_data_label = ctk.CTkLabel(configure_data_section, text="Customize data set", font=("Helvetica", 16))
configure_data_label.pack(side=ctk.TOP, padx=(0,10))

configure_data_button = ctk.CTkButton(configure_data_section, text="Customize", state="disabled", 
                                      command=lambda: open_options_window(on_selections_change=display_select_options, app=app, value_to_add=value_to_add, data_menu=data_menu))
configure_data_button.pack(side=ctk.TOP)


# -Min & Max time section-
MinMax_section = ctk.CTkFrame(app,fg_color="transparent", height=30)
MinMax_section.pack(side=ctk.TOP, fill=ctk.X, expand=True, padx=60, pady=(5,0))

min_label, min_label_value = minmax_frame("Minumum time", MinMax_section)
max_label, max_label_value = minmax_frame("Maximum time", MinMax_section)


# -Loading animation section-
circle_section = ctk.CTkFrame(app, fg_color="transparent")
circle_section.pack(pady=0)

circle1 = ctk.CTkFrame(circle_section, width=11, height=11, fg_color="transparent")
circle1.pack(side=ctk.LEFT, padx=2.5)
circle2 = ctk.CTkFrame(circle_section, width=11, height=11, fg_color="transparent")
circle2.pack(side=ctk.LEFT, padx=2.5)
circle3 = ctk.CTkFrame(circle_section, width=11, height=11, fg_color="transparent")
circle3.pack(side=ctk.LEFT, padx=2.5)


# -Selecting date section-
tabview = ctk.CTkTabview(app, height=215, command=date_uploadig)
tabview.pack(side=ctk.TOP, fill=ctk.X, padx=100, pady=0)

tabview.add("Start")
tabview.add("End")

start_year_entry = sliders_frame("Start", "year - month - day", tabview)
start_year_slider = ctk.CTkSlider(tabview.tab("Start"), height=20, from_=0, to=10, number_of_steps=10, state="disabled", command=lambda value: year_slider_event("start", start_year_slider, start_year_entry, end_year_entry, time_range[0], selected_start_label_year, selected_end_label_year, time_dif, start_hour_entry, end_hour_entry))
start_year_slider.pack(fill=ctk.X, pady=(5,15))


start_hour_entry = sliders_frame("Start", "hour : minute : second", tabview)
start_hour_slider = ctk.CTkSlider(tabview.tab("Start"), height=20, from_=0, to=24*60*2-1, number_of_steps=24*60*2-1, state="disabled", command=lambda value: hour_slider_event("start", str(time_range[0]).split(" ")[1], time_range[0].strftime("%Y-%m-%d"), start_year_entry, end_year_entry, start_hour_entry, end_hour_entry, start_hour_slider, selected_start_label_hour, selected_end_label_hour))
start_hour_slider.pack(fill=ctk.X, pady=(5,0))

end_year_entry = sliders_frame("End", "year - month - day", tabview)
end_year_slider = ctk.CTkSlider(tabview.tab("End"), height=20, from_=0, to=10, number_of_steps=10, state="disabled", command=lambda value: year_slider_event("end", end_year_slider, end_year_entry, start_year_entry, time_range[-1], selected_start_label_year, selected_end_label_year, time_dif, end_hour_entry, start_hour_entry))
end_year_slider.pack(fill=ctk.X, pady=(5,15))

end_hour_entry = sliders_frame("End", "hour : minute : second", tabview)
end_hour_slider = ctk.CTkSlider(tabview.tab("End"), height=20, from_=0, to=24*60*2-1, number_of_steps=24*60*2-1, state="disabled", command=lambda value: hour_slider_event("end", str(time_range[-1]).split(" ")[1], time_range[-1].strftime("%Y-%m-%d"), end_year_entry, start_year_entry, end_hour_entry, start_hour_entry, end_hour_slider, selected_start_label_hour, selected_end_label_hour))
end_hour_slider.pack(fill=ctk.X, pady=(5,0))


# -Lowest plot section-
lowest_section = ctk.CTkFrame(app, fg_color="transparent")
lowest_section.pack(side=ctk.TOP, fill=ctk.X, pady=10, padx=10)

right_section = ctk.CTkFrame(lowest_section, fg_color="transparent")
right_section.pack(side=ctk.RIGHT, fill=ctk.X)


show_plot_button = ctk.CTkButton(right_section, text="Show plot", state="disabled", command=create_plot_handler)
show_plot_button.pack(side=ctk.RIGHT)

left_section = ctk.CTkFrame(lowest_section, fg_color="transparent")
left_section.pack(side=ctk.LEFT, fill=ctk.X)


selected_start_label_year, selected_start_label_hour = selected_time(left_section, "Start: ")

selected_end_label_year, selected_end_label_hour = selected_time(left_section, "End:  ")

time_label_list = [min_label_value, max_label_value, selected_start_label_year, selected_start_label_hour, selected_end_label_year, 
                selected_end_label_hour, start_year_entry, start_hour_entry, end_year_entry, end_hour_entry, start_year_slider, 
                start_hour_slider, end_year_slider, end_hour_slider]

app.mainloop() 