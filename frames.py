import customtkinter as ctk

def minmax_frame(text, MinMax_section): #to
    section = ctk.CTkFrame(MinMax_section, fg_color="transparent")
    section.pack(side=ctk.LEFT, fill=ctk.X, expand=True)

    label = ctk.CTkLabel(section, text=text, font=("Helvetica", 13), text_color="grey")
    label.pack(side=ctk.TOP, fill=ctk.X, padx=35)

    label_value = ctk.CTkLabel(section, text="", font=("Helvetica", 15))
    label_value.pack(side=ctk.TOP, fill=ctk.X, padx=35)

    return label, label_value

def sliders_frame(tab_text, date_text, tabview): #to
    frame = ctk.CTkFrame(tabview.tab(tab_text))
    frame.pack(side=ctk.TOP, pady=5)
    label = ctk.CTkLabel(frame, text=date_text)
    label.pack(side=ctk.LEFT, pady=5)
    entry = ctk.CTkEntry(frame, placeholder_text="", font=("Helvetica", 15), justify="center", border_width=0)
    entry.pack(side=ctk.LEFT, padx=10)
    return entry

def selected_time (parent, text): #to
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(side=ctk.TOP, fill=ctk.X, expand=True)

    label = ctk.CTkLabel(frame, text=text, font=("Helvetica", 12), text_color="grey")
    label.pack(side=ctk.LEFT, fill=ctk.X, padx=(20,0))
    
    label_date = ctk.CTkLabel(frame, text="", font=("Helvetica", 14))
    label_date.pack(side=ctk.LEFT, fill=ctk.X, padx=(15,0))
    
    label_time = ctk.CTkLabel(frame, text="", font=("Helvetica", 14))
    label_time.pack(side=ctk.RIGHT, fill=ctk.X, padx=(15,0))
    return label_date, label_time