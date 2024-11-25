import customtkinter as ctk

def timeLabelClearing(min_label_value, max_label_value, selected_start_label_year, selected_start_label_hour, selected_end_label_year, selected_end_label_hour, 
                      start_year_entry, start_hour_entry, end_year_entry, end_hour_entry, start_year_slider, start_hour_slider, end_year_slider, end_hour_slider):
    
    text = [min_label_value, max_label_value, selected_start_label_year, selected_start_label_hour, selected_end_label_year, selected_end_label_hour]
    [i.configure(text="") for i in text]
    entry = [start_year_entry, start_hour_entry, end_year_entry, end_hour_entry]
    [i.delete(0, ctk.END) for i in entry]
    slider = [start_year_slider, start_hour_slider, end_year_slider, end_hour_slider]
    [i.configure(state="disabled") for i in slider]