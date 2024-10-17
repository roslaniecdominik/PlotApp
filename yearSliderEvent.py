def year_slider_event(id, slider1, entry1, entry2, time, selected_start_label_year, selected_end_label_year):
   
    if entry2.get() !="":

        if entry2.get() == str(time).split()[0]: #the strip moves but doesn't change the label

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