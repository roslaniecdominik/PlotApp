import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog, messagebox
import threading
import pandas as pd
# 

from buttonState import buttonState
from centerWindow import center_window
from dataConfiguration import merge_data, time_column, defining_data
from frames import minmax_frame, sliders_frame, selected_time
from plotCreator import create_plot
from sliderEvent import year_slider_event, hour_slider_event, time_updater
from timeLabelClearing import timeLabelClearing
from solutionGenerator import solution_generator

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
    create_plot(start_year_entry, start_hour_entry, end_year_entry, end_hour_entry, data, selected_data, selected_station_solution, station_list, filepaths, app)

def read_time():
    global data, selected_data, filepath, loading_check, time_range, time_dif

    show_plot_button.configure(state="disabled")

    selected_data = data_menu.get()

    filepath = []
    for key, value in data_dict.items():
        if value == selected_data:
            for i in filepaths_cut:
                with open(i, "r") as file:
                    first_row = file.readline()
                    if key in first_row:
                        filepath.append(i)

    data = pd.read_csv(filepath[0], sep=';', index_col=False, skipinitialspace=True)
    data = time_column(data)
 
    data = merge_data(data, selected_data, filepath)

    
    time_range = [datetime.strptime(str(min(data["datetime"])), "%Y-%m-%d %H:%M:%S"), datetime.strptime(str(max(data["datetime"])), "%Y-%m-%d %H:%M:%S")]

    time_dif = int((time_range[-1] - time_range[0]).days)

    min_label_value.configure(text=min(data["datetime"]))
    max_label_value.configure(text=max(data["datetime"]))
    

    time_updater (time_range[0], start_year_entry, start_hour_entry, start_year_slider, selected_start_label_year,  selected_start_label_hour, time_dif)
    start_minute = (datetime.strptime(time_range[0].strftime("%H:%M:%S"), "%H:%M:%S")).minute * 2
    start_hour_slider.configure(from_= start_minute, to=24*60*2-1, number_of_steps=24*60*2-1 - start_minute)

    time_updater (time_range[-1], end_year_entry, end_hour_entry, end_year_slider, selected_end_label_year, selected_end_label_hour, time_dif)
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

def read_data(event):
    global data_dict, loading_check, filepaths_cut, selected_station_solution

    show_plot_button.configure(state="disabled")

    selected_station_solution = station_menu_fullVAR.get()
    selected_station = selected_station_solution.split(" ")[0]
    selected_solution = solution_generator(selected_station_solution.split("(")[1].split(")")[0])

    filepaths_cut = [filepath for filepath in filepaths if selected_station in filepath and selected_solution in filepath]

    
    data_dict, single_plot, triple_plot = defining_data()

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
    
    data_menu.configure(values=value_to_add)

    optionmenu_var = ctk.StringVar(value="Data..")
    data_menu.configure(variable=optionmenu_var)


    loading_check = False
    loading_animation()

    timeLabelClearing(*time_label_list)
    buttonState([data_menu])

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


def open_file():
    global filepaths, loading_check
    filepaths = filedialog.askopenfilenames(filetypes=[("Text files", "*.log")])
    loading_check = True
    loading_animation()
    loading_station = threading.Thread(target=read_station)
    loading_station.start()
    show_plot_button.configure(state="disabled")


# -Main window-
ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()
app.title("PlotApp")

center_window(app, 700, 500)

# -File section-
file_section = ctk.CTkFrame(app, fg_color="transparent")
file_section.pack(side=ctk.TOP, fill=ctk.BOTH, padx=55, pady=10)
open_file_button = ctk.CTkButton(file_section, text="Upload file", width=100, bg_color="transparent", command=open_file)
open_file_button.pack(side=ctk.LEFT, fill=ctk.BOTH)
filename_entry = ctk.CTkEntry(file_section, border_width=0)
filename_entry.pack(side=ctk.RIGHT, fill=ctk.BOTH, padx=(10,0), expand=True)

# -Station & data section-
station_fullLabel = ctk.CTkLabel(app, text=" ", font=("Helvetica", 12))
station_fullLabel.pack(side=ctk.TOP)


StationData_section = ctk.CTkFrame(app, border_width=0, corner_radius=10, fg_color="transparent")
StationData_section.pack(side=ctk.TOP, fill=ctk.X, padx=55, pady=(10,20))

station_section = ctk.CTkFrame(StationData_section, border_width=0, corner_radius=10, fg_color="transparent")
station_section.pack(side=ctk.LEFT, fill=ctk.X)

station_label = ctk.CTkLabel(station_section, text="Select station", font=("Helvetica", 18))
station_label.pack(side=ctk.LEFT, padx=(0,10))


station_menu_fullVAR = ctk.StringVar(station_section)
station_menu_variable = ctk.StringVar(value="...")
station_menu = ctk.CTkOptionMenu(station_section, width=150, values=[], variable=station_menu_variable, state="disabled", command=read_data_in_thread)
station_menu.pack(side=ctk.RIGHT,)


data_section = ctk.CTkFrame(StationData_section, border_width=0, corner_radius=10, fg_color="transparent")
data_section.pack(side=ctk.RIGHT, fill=ctk.X)

data_label = ctk.CTkLabel(data_section, text="Select data", font=("Helvetica", 18))
data_label.pack(side=ctk.LEFT, padx=(0,10))

data_menu_variable = ctk.StringVar(value="...")
data_menu = ctk.CTkOptionMenu(data_section, width=150, values=[], variable=data_menu_variable, state="disabled", command=read_time_in_thread)
data_menu.pack(side=ctk.RIGHT)


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