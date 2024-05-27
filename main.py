import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox
import threading
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


# -- PLOT CONFIGURATION --
data_dict = {"PDop": "DOP factors", 
            "RecX": "REC XYZ", 
            "RecmX": "RECm XYZ", 
            "mIonDel": "ION"}

single_plot = ["DOP factors", "ION"]
triple_plot = ["REC XYZ", "RECm XYZ"]


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def match_data(data):
    match data:
        case "DOP factors":
            data_listname = ["PDop", "TDop", "HDop", "VDop", "GDop"]
            data_colors = ["red", "green", "blue", "yellow", "orange"]
        case "REC XYZ":
            data_listname = ["RecX", "RecY", "RecZ"]
            data_colors = ["red", "green", "blue"]
        case "RECm XYZ":
            data_listname = ["RecmX", "RecmY", "RecmZ"]
            data_colors = ["red", "green", "blue"]
        case "ION":
            data_listname = ["mIonDel"]
            data_colors = ["red"]
    return data_listname, data_colors

def date_uploadig():
    if tabview.get() == "Start" and end_year_entry.get() == str(time[0]).split()[0]:
        start_year_entry.delete(0, ctk.END)
        start_year_entry.insert(0, end_year_entry.get())
    elif tabview.get() == "End" and start_year_entry.get() == str(time[-1]).split()[0]:
        end_year_entry.delete(0, ctk.END)
        end_year_entry.insert(0, start_year_entry.get())

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

def merge_data():
    global data

    data_listname, x = match_data(selected_data)

    if len(filepath) > 2:
        data_to_merge = data
        data_listname.append("datetime")
        data_to_merge = data_to_merge[data_listname]
        for i in range(len(filepath)-1):
            if i < (len(filepath)-2): 
                data = pd.read_csv(filepath[i+1], sep=';', index_col=False, skipinitialspace=True)
                data = time_column(data)
                data = data[data_listname]
                merged = pd.concat([data_to_merge, data])
                data_to_merge = merged
        data = merged

def year_slider_event(id, slider1, entry1, entry2, time):
   
    if entry2.get() !="":

        if entry2.get() == str(time).split()[0]: #pasek się rusza ale nie zmienia etykiety

            if id == "start":
                selected_start_label_year.configure(text=entry2.get())
            elif id == "end":
                selected_end_label_year.configure(text=entry2.get())
            pass

        else:
            year = datetime.strptime(entry2.get(), "%Y-%m-%d")
            if id == "start":
                slider1.configure(from_=0, to=int((year - time).days+1), number_of_steps=int((year - time).days)+1)
                selected_date = time + timedelta(days=slider1.get())

            elif id == "end":
                slider1.configure(from_=0, to=int((time - year).days), number_of_steps=int((time - year).days))
                selected_date = year + timedelta(days=slider1.get())

            entry1.delete(0, ctk.END)
            entry1.insert(0, selected_date.strftime("%Y-%m-%d"))
    else:
        slider1.configure(from_=0, to=time_dif, number_of_steps=time_dif)
        selected_date = time + timedelta(days=slider1.get())
        entry1.delete(0, ctk.END)
        entry1.insert(0, selected_date.strftime("%Y-%m-%d"))

    if id == "start" and entry2.get() != str(time).split()[0]:
        selected_start_label_year.configure(text=selected_date.strftime("%Y-%m-%d"))
    elif id == "end" and entry2.get() != str(time).split()[0]:
        selected_end_label_year.configure(text=selected_date.strftime("%Y-%m-%d"))
       
def hour_slider_event(id, time, date, year_entry1, year_entry2, hour_entry1, hour_entry2, slider1):

    if year_entry1.get() == year_entry2.get() and hour_entry2.get() == time:
        pass

    elif year_entry1.get() == date and year_entry1.get() == year_entry2.get():
        parts_from = (str(time)).split(":")
        hours_from = int(parts_from[0])
        minutes_from = int(parts_from[1])
        seconds_from = int(parts_from[2])
        if seconds_from == 30:
            hour_from = (hours_from*60 + minutes_from)*2+1
        else:
            hour_from = (hours_from*60 + minutes_from)*2

        parts_to = (hour_entry2.get()).split(":")
        hours_to = int(parts_to[0])
        minutes_to = int(parts_to[1])
        seconds_to = int(parts_to[2])
        if seconds_to == 30:
            hour_to = (hours_to*60 + minutes_to)*2+1
        else:
            hour_to = (hours_to*60 + minutes_to)*2

        

        if id == "start":
            slider1.configure(from_=hour_from, to=hour_to, number_of_steps=hour_to - hour_from)

            start_hour = datetime.strptime("0:00:00", '%H:%M:%S').time()
            start_hour = datetime.combine(datetime.today(), start_hour)

            selected_date = (start_hour + timedelta(seconds=slider1.get()*30)).time()

            selected_start_label_hour.configure(text=selected_date)
        elif id =="end":
            slider1.configure(from_=hour_to, to=hour_from, number_of_steps=hour_from - hour_to)

            start_hour = datetime.strptime("0:00:00", '%H:%M:%S').time()
            start_hour = datetime.combine(datetime.today(), start_hour)

            selected_date = (start_hour + timedelta(seconds=slider1.get()*30)).time()
            selected_end_label_hour.configure(text=selected_date)

        hour_entry1.delete(0, ctk.END)
        hour_entry1.insert(0, selected_date)

    elif year_entry1.get() == date:
        parts = (str(time)).split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        if seconds == 30:
            hour = (hours*60 + minutes)*2+1
        else:
            hour = (hours*60 + minutes)*2

        if id == "start":
            slider1.configure(from_=hour, to=24*60*2-1, number_of_steps=24*60*2-1 - hour)

            start_hour = datetime.strptime("0:00:00", '%H:%M:%S').time()
            start_hour = datetime.combine(datetime.today(), start_hour)

            selected_date = (start_hour + timedelta(seconds=slider1.get()*30)).time()

            selected_start_label_hour.configure(text=selected_date)

        elif id =="end":
            slider1.configure(from_=0, to=hour, number_of_steps=hour)
            
            start_hour = datetime.strptime("0:00:00", '%H:%M:%S').time()
            start_hour = datetime.combine(datetime.today(), start_hour)
            selected_date = (start_hour + timedelta(seconds=slider1.get()*30)).time()

            selected_end_label_hour.configure(text=selected_date)

        hour_entry1.delete(0, ctk.END)
        hour_entry1.insert(0, selected_date)

    elif year_entry1.get() == year_entry2.get():

        parts = hour_entry2.get().split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        if seconds == 30:
            hour = (hours*60 + minutes)*2+1
        else:
            hour = (hours*60 + minutes)*2

        if id == "start":
            slider1.configure(from_=0, to=hour, number_of_steps=hour)
            
            start_hour = datetime.strptime("0:00:00", '%H:%M:%S').time()
            start_hour = datetime.combine(datetime.today(), start_hour)
            selected_date = (start_hour + timedelta(seconds=slider1.get()*30)).time()
            
            selected_start_label_hour.configure(text=selected_date)

        elif id =="end":
            start_hour = datetime.strptime(hour_entry2.get(), '%H:%M:%S').time()

            slider1.configure(from_=0, to=24*60*2-1 - hour, number_of_steps=(24*60*2-1 - hour))

            start_hour = datetime.combine(datetime.today(), start_hour)
            selected_date = (start_hour + timedelta(seconds=slider1.get()*30)).time()

            selected_end_label_hour.configure(text=selected_date)

        hour_entry1.delete(0, ctk.END)
        hour_entry1.insert(0, selected_date)
        
        
    else:
        if id =="start":
            start_hour = datetime.strptime("0:00:00", '%H:%M:%S').time()
            start_hour = datetime.combine(datetime.today(), start_hour)
            selected_date = (start_hour + timedelta(seconds=slider1.get()*30)).time()

            selected_start_label_hour.configure(text=selected_date)

        if id =="end":
            start_hour = datetime.strptime("0:00:00", '%H:%M:%S').time()
            start_hour = datetime.combine(datetime.today(), start_hour)
            selected_date = (start_hour + timedelta(seconds=slider1.get()*30)).time()

            selected_end_label_hour.configure(text=selected_date)
            
        slider1.configure(from_=0, to=24*60*2-1, number_of_steps=24*60*2-1)
        hour_entry1.delete(0, ctk.END)
        hour_entry1.insert(0, selected_date)

def state_changing(list):
        for i in list:
            i.configure(state="normal")

def timeLabel_clearing():
        text = [min_label_value, max_label_value, selected_start_label_year, selected_start_label_hour, selected_end_label_year, selected_end_label_hour]
        [i.configure(text="") for i in text]

        entry = [start_year_entry, start_hour_entry, end_year_entry, end_hour_entry]
        [i.delete(0, ctk.END) for i in entry]

        slider = [start_year_slider, start_hour_slider, end_year_slider, end_hour_slider]
        [i.configure(state="disabled") for i in slider]


def loading_animation():
    global color_index, loading_check
    
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
color_index = 0     
colors = [("grey", "transparent", "transparent"), ("transparent", "grey", "transparent"), ("transparent", "transparent", "grey"), ("transparent", "grey", "transparent")]

#------------------------


def create_plot():
    global loading_check

    def toggle_visibility(name):
        name.set_visible(not name.get_visible())
        plt.draw()

    start_time = f"{start_year_entry.get()} {start_hour_entry.get()}"
    end_time = f"{end_year_entry.get()} {end_hour_entry.get()}"

    if start_time > end_time:
        messagebox.showinfo("Message", "Starting time must be less than end time")

    else:
        time_data = data.loc[(data['datetime'] >= start_time) & (data['datetime'] <= end_time)]

        time_diff = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

        if (time_diff > timedelta(days=365*2)):
            xaxis_set = "%y"
            xaxis_label = "TIME [year]"
        elif (time_diff <= timedelta(days=365*2)) and (time_diff > timedelta(days=6*31)):
            xaxis_set = "%y-%m"
            xaxis_label = "TIME [year-month]"
        elif (time_diff <= timedelta(days=6*31)) and (time_diff > timedelta(days=2*31)):
            xaxis_set = "%m-%d"
            xaxis_label = "TIME [month-day]"
        elif (time_diff <= timedelta(days=2*31)) and (time_diff > timedelta(days=31)):
            xaxis_set = "%m-%d %H"
            xaxis_label = "TIME [month-day hour]"
        elif (time_diff <= timedelta(days=31)) and (time_diff > timedelta(days=1)):
            xaxis_set = "%d %H:%M"
            xaxis_label = "TIME [day hour:min]"
        elif (time_diff <= timedelta(hours=24)) and (time_diff > timedelta(hours=1)):
            xaxis_set = "%H:%M"
            xaxis_label = "TIME [hour:min]"
        elif time_diff < timedelta(minutes=60):
            xaxis_set = "%M:%S"
            xaxis_label = "TIME [min:sec]"
        else:
            xaxis_set = "%Y-%m-%d %H:%M"
            xaxis_label = "TIME [year-month-day hour:min]"


        if selected_data in single_plot:

            def plot():
                fig, ax = plt.subplots(figsize=(10,6))
                
                plots = {}
                plot_objects = []

                for layer_name, color in zip(data_listname, data_colors):
                    plots[layer_name], = ax.plot(time_data["datetime"], time_data[layer_name], color=color, linewidth=1, label=layer_name)
                    plot_objects.append(plots[layer_name])

                ax.set_title(selected_data, font="Verdana", fontsize=14, fontweight="light")
                ax.set_xlabel(xaxis_label, font="Verdana")
                ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
                ax.grid(True)
                ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                ax.ticklabel_format(useOffset=False, axis='y', style='plain')
                extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                ax.text(-0.12, 1.10, f"{selected_station}, {extend_time}", transform=ax.transAxes, va='top', ha='left', fontsize=11)

                return plot_objects, fig, ax
            
            def layer_buttons(ax):
                for i, layer_name in enumerate(data_listname):
                    layer_frame = ctk.CTkFrame(layers_frame)
                    layer_frame.pack(anchor="w", padx=10, pady=5)

                    # Buttons
                    toggle_button = ctk.CTkCheckBox(layer_frame, text=layer_name, command=lambda idx=i: toggle_visibility(data_list[idx]))
                    toggle_button.grid(row=0, column=0)
                    toggle_button.select()

                    # Buttons line
                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=data_colors[i])
                    buttons_line.grid(row=0, column=1, padx=(5, 5))

        elif selected_data in triple_plot:
            def plot():
                fig, ax = plt.subplots(3, 1, figsize=(10,6))
                
                for i, layer_name in enumerate(data_listname):
                    line, = ax[i].plot(time_data["datetime"], time_data[layer_name], color=data_colors[i], linewidth=1, label=layer_name)
                    ax[i].set_title(layer_name)
                    ax[i].xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter(xaxis_set))
                    ax[i].grid(True)
                    ax[i].legend(loc='center left', bbox_to_anchor=(1, 0.5))
                    ax[i].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
                    ax[i].ticklabel_format(useOffset=False, axis='y', style='plain')

                extend_time = f"{datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")}  -  {datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")}"
                ax[0].text(-0.2, 1.5, f"{selected_station}, {extend_time}", transform=ax[0].transAxes, va='top', ha='left', fontsize=11)
                ax[0].text(-0.1, 1.2, '{:>13}'.format('[m]'), transform=ax[0].transAxes, va='top', ha='left', fontsize=10)
                ax[-1].set_xlabel(xaxis_label, font="Verdana")

                fig.tight_layout()
                plot_objects = []
                return plot_objects, fig, ax

            def layer_buttons(ax):
                for i, ax in enumerate(ax):
                    layer_frame = ctk.CTkFrame(layers_frame)
                    layer_frame.pack(anchor="w", padx=10, pady=5)

                    # Buttons
                    toggle_button = ctk.CTkCheckBox(layer_frame, text=data_listname[i], command=lambda line=ax.get_lines()[0]: toggle_visibility(line))
                    toggle_button.grid(row=0, column=0)
                    toggle_button.select()

                    # Buttons line
                    buttons_line = ctk.CTkFrame(layer_frame, width=50, height=5, fg_color=data_colors[i])
                    buttons_line.grid(row=0, column=2, padx=(0, 5))

        data_listname, data_colors = match_data(selected_data)

        plot_objects, fig, ax = plot()
        data_list = plot_objects

        new_window = ctk.CTkToplevel(app)
        new_window.title("PLOT")

        center_window(new_window, 1200, 650)

        layers_frame = ctk.CTkFrame(new_window,)
        layers_frame.pack(side=ctk.RIGHT, fill=ctk.Y)

        label = ctk.CTkLabel(layers_frame, text="Layers", font=("Helvetica", 22))
        label.pack(side=ctk.TOP, fill=ctk.X, pady=(10, 50))

        # Layer buttons
        layer_buttons(ax)

        canvas_plot = FigureCanvasTkAgg(fig, master=new_window)
        canvas_plot.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas_plot, new_window)
        toolbar.update()

def read_time():
    global data, selected_data, filepath, loading_check, time, time_dif

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

    merge_data()

    #----------- MIN MAX SECTION
    if len(filepath) > 1:
        data_last = pd.read_csv(filepath[-1], sep=';', index_col=False, skipinitialspace=True)
        data_last = time_column(data_last)
        merged = pd.concat([data, data_last])
       
        data = merged
    
    time = [datetime.strptime(str(min(data["datetime"])), "%Y-%m-%d %H:%M:%S"), datetime.strptime(str(max(data["datetime"])), "%Y-%m-%d %H:%M:%S")]
    time_dif = int((time[-1] - time[0]).days)

    min_label_value.configure(text=min(data["datetime"]))
    max_label_value.configure(text=max(data["datetime"]))
    
    def time_updater (time, year_entry, hour_entry, year_slider, selected_year_label, selected_hour_label):
        year_entry.delete(0, ctk.END)
        year_entry.insert(0, time.strftime("%Y-%m-%d"))
        
        hour_entry.delete(0, ctk.END)
        hour_entry.insert(0, time.strftime("%H:%M:%S"))

        year_slider.configure(from_=0, to=time_dif, number_of_steps=time_dif)

        selected_year_label.configure(text=time.strftime("%Y-%m-%d"))
        selected_hour_label.configure(text=time.strftime("%H:%M:%S"))

    time_updater (time[0], start_year_entry, start_hour_entry, start_year_slider, selected_start_label_year,  selected_start_label_hour)
    start_minute = (datetime.strptime(time[0].strftime("%H:%M:%S"), "%H:%M:%S")).minute * 2
    start_hour_slider.configure(from_= start_minute, to=24*60*2-1, number_of_steps=24*60*2-1 - start_minute)

    time_updater (time[-1], end_year_entry, end_hour_entry, end_year_slider, selected_end_label_year, selected_end_label_hour)
    end_minute = (datetime.strptime(time[-1].strftime("%H:%M:%S"), "%H:%M:%S")).minute * 2
    end_hour_slider.configure(from_=0, to=24*60*2-1-end_minute, number_of_steps=24*60*2-1 - end_minute)

    loading_check = False
    loading_animation()

    state_changing([show_plot_button, start_hour_slider, end_hour_slider])
    
    if time_dif != 0:
        state_changing([start_year_slider, end_year_slider])

def read_time_in_thread(event):
    global loading_check
    loading_check = True
    app.after(500, loading_animation)
    threading.Thread(target=read_time).start()

def read_data(event):
    global data_dict, loading_check, filepaths_cut, selected_station

    show_plot_button.configure(state="disabled")

    selected_station = station_menu.get()
    filepaths_cut = [filepath for filepath in filepaths if selected_station in filepath]

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

    timeLabel_clearing()
    state_changing([data_menu])

def read_data_in_thread(event):
    global loading_check

    loading_check = True
    app.after(500, loading_animation)
    threading.Thread(target=read_data, args=(event,)).start()

def read_station():
    global loading_check

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

                digit_id = filepath.find(next(filter(str.isdigit, filepath[slash_id:])))
                station = filepath[slash_id + 1: digit_id]

                if station not in station_list:
                    station_list.append(station)

        except: #messagebox "wrong file name"
            print("WRONG FILE NAME")

        show_plot_button.configure(state="disabled")
        return(station_list)
    
    loading_check = False
    loading_animation()

    if filepaths != "":
        station_list = station_finder(filepaths)
        station_menu.configure(values=station_list)

        optionmenu_var = ctk.StringVar(value="Station..")
        station_menu.configure(variable=optionmenu_var)

 
    timeLabel_clearing()

    state_changing([station_menu])

def open_file():
    global filepaths, loading_check
    filepaths = filedialog.askopenfilenames(filetypes=[("Text files", "*.log")])
    loading_check = True
    app.after(500, loading_animation)

    loading_station = threading.Thread(target=read_station)
    loading_station.start()
    show_plot_button.configure(state="disabled")


# -Main window-
ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()
app.title("PlotApp")

center_window(app, 675, 475)

# -File section-
file_section = ctk.CTkFrame(app, fg_color="transparent")
file_section.pack(side=ctk.TOP, fill=ctk.BOTH, padx=55, pady=10)
open_file_button = ctk.CTkButton(file_section, text="Load file", width=100, bg_color="transparent", command=open_file)
open_file_button.pack(side=ctk.LEFT, fill=ctk.BOTH)
filename_entry = ctk.CTkEntry(file_section, border_width=0)
filename_entry.pack(side=ctk.RIGHT, fill=ctk.BOTH, padx=(10,0), expand=True)

# -Station & data section-
StationData_section = ctk.CTkFrame(app, border_width=0, corner_radius=10, fg_color="transparent")
StationData_section.pack(side=ctk.TOP, fill=ctk.X, padx=55, pady=20)

station_section = ctk.CTkFrame(StationData_section, border_width=0, corner_radius=10, fg_color="transparent")
station_section.pack(side=ctk.LEFT, fill=ctk.X)

station_label = ctk.CTkLabel(station_section, text="Select station", font=("Helvetica", 18))
station_label.pack(side=ctk.LEFT, padx=(0,10))

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
MinMax_section.pack(side=ctk.TOP, fill=ctk.X, expand=True, padx=100, pady=(5,0))

def minmax_frame(text):
    section = ctk.CTkFrame(MinMax_section, fg_color="transparent")
    section.pack(side=ctk.LEFT, fill=ctk.X, expand=True)

    label = ctk.CTkLabel(section, text=text, font=("Helvetica", 13), text_color="grey")
    label.pack(side=ctk.TOP, fill=ctk.X, padx=35)

    label_value = ctk.CTkLabel(section, text="", font=("Helvetica", 15))
    label_value.pack(side=ctk.TOP, fill=ctk.X, padx=35)

    return label, label_value

min_label, min_label_value = minmax_frame("Minumum time")
max_label, max_label_value = minmax_frame("Maximum time")


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

time = [0]
time_dif = 0

def sliders_frame(tab_text, date_text):
    frame = ctk.CTkFrame(tabview.tab(tab_text))
    frame.pack(side=ctk.TOP, pady=5)
    label = ctk.CTkLabel(frame, text=date_text)
    label.pack(side=ctk.LEFT, pady=5)
    entry = ctk.CTkEntry(frame, placeholder_text="", font=("Helvetica", 15), justify="center", border_width=0)
    entry.pack(side=ctk.LEFT, padx=10)
    return entry

start_year_entry = sliders_frame("Start", "year - month - day")
start_year_slider = ctk.CTkSlider(tabview.tab("Start"), height=20, from_=0, to=10, number_of_steps=10, state="disabled", command=lambda value: year_slider_event("start", start_year_slider, start_year_entry, end_year_entry, time[0]))
start_year_slider.pack(fill=ctk.X, pady=(5,15))

start_hour_entry = sliders_frame("Start", "hour : minute : second")
start_hour_slider = ctk.CTkSlider(tabview.tab("Start"), height=20, from_=0, to=24*60*2-1, number_of_steps=24*60*2-1, state="disabled", command=lambda value: hour_slider_event("start", str(time[0]).split(" ")[1], time[0].strftime("%Y-%m-%d"), start_year_entry, end_year_entry, start_hour_entry, end_hour_entry, start_hour_slider))
start_hour_slider.pack(fill=ctk.X, pady=(5,0))

end_year_entry = sliders_frame("End", "year - month - day")
end_year_slider = ctk.CTkSlider(tabview.tab("End"), height=20, from_=0, to=10, number_of_steps=10, state="disabled", command=lambda value: year_slider_event("end", end_year_slider, end_year_entry, start_year_entry, time[-1]))
end_year_slider.pack(fill=ctk.X, pady=(5,15))

end_hour_entry = sliders_frame("End", "hour : minute : second")
end_hour_slider = ctk.CTkSlider(tabview.tab("End"), height=20, from_=0, to=24*60*2-1, number_of_steps=24*60*2-1, state="disabled", command=lambda value: hour_slider_event("end", str(time[-1]).split(" ")[1], time[-1].strftime("%Y-%m-%d"), end_year_entry, start_year_entry, end_hour_entry, start_hour_entry, end_hour_slider))
end_hour_slider.pack(fill=ctk.X, pady=(5,0))


# -Lowest plot section-
lowest_section = ctk.CTkFrame(app, fg_color="transparent")
lowest_section.pack(side=ctk.TOP, fill=ctk.X, pady=10, padx=10)

right_section = ctk.CTkFrame(lowest_section, fg_color="transparent")
right_section.pack(side=ctk.RIGHT, fill=ctk.X)

show_plot_button = ctk.CTkButton(right_section, text="Show plot", state="disabled", command=create_plot)
show_plot_button.pack(side=ctk.RIGHT)

left_section = ctk.CTkFrame(lowest_section, fg_color="transparent")
left_section.pack(side=ctk.LEFT, fill=ctk.X)

def selected_time (parent, text):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(side=ctk.TOP, fill=ctk.X, expand=True)

    label = ctk.CTkLabel(frame, text=text, font=("Helvetica", 12), text_color="grey")
    label.pack(side=ctk.LEFT, fill=ctk.X, padx=(20,0))
    
    label_date = ctk.CTkLabel(frame, text="", font=("Helvetica", 14))
    label_date.pack(side=ctk.LEFT, fill=ctk.X, padx=(15,0))
    
    label_time = ctk.CTkLabel(frame, text="", font=("Helvetica", 14))
    label_time.pack(side=ctk.RIGHT, fill=ctk.X, padx=(15,0))
    return label_date, label_time

selected_start_label_year, selected_start_label_hour = selected_time(left_section, "Start: ")

selected_end_label_year, selected_end_label_hour = selected_time(left_section, "End:  ")

app.mainloop()