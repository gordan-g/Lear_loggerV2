import tkinter as tk
from tkinter import *
import function

testing = tk.Tk()
testing.title("Logger")
testing.configure(background="#C1CDCD")

def change_entry_state():
    if Checkbutton5.get() == 1:
        fyon_entry.delete(0, tk.END)
        fyon_entry.config(state=DISABLED)
    else:
        fyon_entry.config(state=NORMAL)


date_label = tk.Label(testing, text="Unesite datum u formatu: YYYY-MM-DD", font=("Arial", 20))
date_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
date_entry = tk.Entry(testing, width=20, font=('Arial 15'))
date_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
date_entry.focus_set()

fyon_label = tk.Label(testing, text="Unesite FYON", font=("Arial", 20))
fyon_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
fyon_entry = tk.Entry(testing, width=20, font=('Arial 15'))
fyon_entry.place(relx=0.5, rely=0.30, anchor=tk.CENTER)

options = ['IP Novi Sad', 'WH Novi Sad', 'UNI1 Novi Sad', 'UNI2 Novi Sad']

choose = StringVar()
choose.set('IP Novi Sad')

drop_down_label = tk.Label(testing, text="Izaberite familiju iz padajuceg menija", font=("Arial", 20))
drop_down_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
drop_down = OptionMenu(testing, choose, *options)
drop_down.place(relx=0.5, rely=0.50, anchor=tk.CENTER)


Checkbutton5 = IntVar()
Button5 = Checkbutton(testing, text="Log file za citav dan",
                      variable=Checkbutton5,
                      onvalue=1,
                      command=change_entry_state,
                      offvalue=0,
                      height=2,
                      width=30,
                      font=("Arial", 15))

Button5.place(relx=0.5, rely=0.65, anchor=tk.CENTER)


start_button = tk.Button(testing, text="Start", command=lambda: function.executor(fyon=fyon_entry.get(), datum=date_entry.get(), whole_day=Checkbutton5.get(), chosen_family = choose.get()), width=30, height=3, bg='green')
start_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

close_button = tk.Button(testing, text="Zatvori program", command= lambda : testing.destroy(), bg ="red", width=30, height=3)
close_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

testing.attributes('-fullscreen', True)
testing.mainloop()
