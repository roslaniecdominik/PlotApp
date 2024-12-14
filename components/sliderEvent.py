import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection
from datetime import datetime, timedelta
import pandas as pd

def time_updater (time, year_entry, hour_entry, year_slider, selected_year_label, selected_hour_label, time_dif):
        year_entry.delete(0, ctk.END)
        year_entry.insert(0, time.strftime("%Y-%m-%d"))
        
        hour_entry.delete(0, ctk.END)
        hour_entry.insert(0, time.strftime("%H:%M:%S"))

        year_slider.configure(from_=0, to=time_dif, number_of_steps=time_dif)

        selected_year_label.configure(text=time.strftime("%Y-%m-%d"))
        selected_hour_label.configure(text=time.strftime("%H:%M:%S"))

def year_slider_event(id, slider1, entry1, entry2, time, selected_start_label_year, selected_end_label_year, time_dif, hour_label1, hour_label2):
    

    if entry2.get() !="":
        if entry2.get() == str(time).split()[0]:

            year = datetime.strptime(entry2.get(), "%Y-%m-%d")

            if id == "start":
                slider1.configure(from_=0, to=int((year - time).days)+1, number_of_steps=int((year - time).days)+1)
                selected_start_label_year.configure(text=entry2.get())
            elif id == "end":
                slider1.configure(from_=0, to=int((time - year).days)+1, number_of_steps=int((time - year).days+1))
                selected_end_label_year.configure(text=entry2.get())
            pass

        else:
            year = datetime.strptime(entry2.get(), "%Y-%m-%d")

            if id == "start":
                if hour_label1.get() > hour_label2.get():
                    slider1.configure(from_=0, to=int((year - time).days), number_of_steps=int((year - time).days))
                    selected_date = time + timedelta(days=slider1.get())
                else:
                    slider1.configure(from_=0, to=int((year - time).days)+1, number_of_steps=int((year - time).days)+1)
                    selected_date = time + timedelta(days=slider1.get())

            elif id == "end":
                if hour_label1.get() < hour_label2.get():
                    slider1.configure(from_=0, to=int((time - year).days-1), number_of_steps=int((time - year).days-1))
                    selected_date = year + timedelta(days=(slider1.get()+1))
                else:
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

def hour_slider_event(id, time, date, year_entry1, year_entry2, hour_entry1, hour_entry2, slider1, selected_start_label_hour, selected_end_label_hour): 

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

def plot_updater_slider(value,  lines, axss, data_listnames, canvas_plot, cut_data, station_range_text, selected_station, selected_secondStation_solution, cord_time, cord1, cord2, sol_df, entry):

            invisible_lines = cord_time
            start_index = int(value)
            extend_time = f"{str(cut_data.iloc[start_index]['datetime'])}  -  {str(cut_data.iloc[-1]['datetime'])}"
            data_listnames = [el for list in data_listnames for el in list]
            
            entry.delete(0, ctk.END)
            entry.insert(0, cut_data.loc[start_index, "datetime"])

            scatter_symbols = ["mN_", "C_", "N_", "L_", "PRN"]
            invisible_datas = []
            
            for scatter_symbol in scatter_symbols:

                if any(column.startswith(scatter_symbol) for column in cut_data.columns):
                    invisible_data = [0 for _ in range(cut_data[start_index:].shape[0])]
                    invisible_data[0] = cut_data[start_index:][[col for col in cut_data[start_index:].columns if col.startswith(scatter_symbol)]].min().min()
                    invisible_data[-1] = cut_data[start_index:][[col for col in cut_data[start_index:].columns if col.startswith(scatter_symbol)]].max().max()
                    invisible_datas.append(invisible_data)

            for data_listname, line in zip(data_listnames, lines):
                if type(axss) == "s":#np.ndarray:
                    if axss.ndim == 1: #one column
                        for line, ax, data_column in zip(lines, axss, data_listname):
                            line.set_data(cut_data['datetime'][start_index:], cut_data[data_column][start_index:])
                            ax.relim()
                            ax.autoscale_view()
                        station_range_text.set_text(f"{selected_station}, {extend_time}")
                    if axss.ndim == 2:
                        extend_time = f"{str(cord_time.iloc[start_index])}  -  {str(cord_time.iloc[-1])}"

                        #xy
                        for i, (line1, line2) in enumerate([lines[0], lines[2], lines[4]]):
                            line1[0].set_data(cord_time[start_index:], cord1[start_index:])
                            line2[0].set_data(cord_time[start_index:], cord2[start_index:])
                            axss[i, 0].relim()
                            axss[i, 0].autoscale_view()
                            station_range_text.set_text(f"{selected_station} vs {selected_secondStation_solution}      {extend_time}")

                        #compare
                        for i, line in enumerate([lines[1], lines[3], lines[5]], start=3):
                            line.set_data(cord_time[start_index:], sol_df[layer_name][start_index:],)
                            axss[i - 3, 1].relim()
                            axss[i - 3, 1].autoscale_view()
                        
                else:
                    if selected_secondStation_solution != "":
                        invisible_lines = data_listname

                        extend_time = f"{str(cord_time.iloc[start_index]["datetime"])} - {str(cord_time.iloc[-1]["datetime"])}"
                        x_axss = cord1
                        y_axss = cord2
                        x_axss2 = sol_df
                        y_axss2 = layer_name

                        lines[0].set_offsets(list(zip(x_axss[start_index:], y_axss[start_index:])))
                        lines[1].set_offsets(list(zip(x_axss2[start_index:], y_axss2[start_index:])))
                        invisible_lines[0].set_data(x_axss[start_index:], y_axss[start_index:])
                        invisible_lines[1].set_data(x_axss2[start_index:], y_axss2[start_index:])
                        axss.relim()
                        axss.autoscale_view()
                        station_range_text.set_text(f"{selected_station} vs {selected_secondStation_solution}      {extend_time}")

                        
                    else:
                        if isinstance(line, PathCollection):
                            line.set_offsets(list(zip(cut_data['datetime'][start_index:], cut_data[data_listname][start_index:])))
                            for invisible_line, invisible_data in zip(invisible_lines, invisible_datas):
                                invisible_line.set_data(cut_data['datetime'][start_index:], invisible_data)

                        elif isinstance(line, plt.Line2D):
                            # wszystkie single liniowe, działa pojedyńczy triple, działa podwójny triple, działa mix triple z single
                            line.set_data(cut_data['datetime'][start_index:], cut_data[data_listname][start_index:])

                        for axs in axss:
                            axs.set_xlim(cut_data["datetime"][start_index:].min() - 0.01*(cut_data["datetime"].max() - cut_data["datetime"].min()), 
                                         cut_data["datetime"][start_index:].max() + 0.01*(cut_data["datetime"].max() - cut_data["datetime"].min()))
                            axs.relim()
                            axs.autoscale_view()
                        station_range_text.set_text(f"{selected_station}, {extend_time}")
            canvas_plot.draw()