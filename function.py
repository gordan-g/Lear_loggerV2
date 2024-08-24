import subprocess
import pickle
import pandas as pd
import numpy as np
from ping3 import ping
from tkinter import messagebox
import datetime
import os
import shutil

#UNI1 je blizi cutingu, UNI2 je blizi WH liniji.


#Objedinjuje sve funkcije potrebne za dobijanje log fila-a
def executor(datum, whole_day, fyon, chosen_family):

    if not fyon: #Ako je cekirano log za citav dan ovde ce ga setovati na "None"
        fyon = "None"

    wtr_folder = return_table_wtr_storage(chosen_family, datum, whole_day, fyon)

    if wtr_folder:
        wanted_wtr_location = find_exact_wtr(wtr_folder, datum)
    else:
        pass

    try:
        if wanted_wtr_location:
            export_data_from_db(datum, wanted_wtr_location, fyon, chosen_family)
            export_data_to_excel(fyon)
        else:
            pass

    except UnboundLocalError:
        print("Nije dobijena konacna lokacija wtr file-a!")

#Vraca lokaciju gde se nalaze wtr file-ovi izabranog stola.
#pinguje recunar da bi proverio da li je racunar online, ukoliko jeste vraca lokaciju pomenutu u proslom koraku, pod uslovom da su fyon i datum u dobrom formatu.
def return_table_wtr_storage(chosen_family, datum, whole_day, fyon):

    home_dir_dict = {'IP Novi Sad': r'\\NVS-20-1593\c$', 'WH Novi Sad': r'\\NVS-20-1595\c$', 'UNI1 Novi Sad': r'\\GOD-20-1282\c$', 'UNI2 Novi Sad': r'\\GOD-20-1293\c$'}
    table_ip = {'IP Novi Sad': r'10.54.134.155', 'WH Novi Sad': r'10.54.134.156', 'UNI1 Novi Sad': r'10.54.134.157', 'UNI2 Novi Sad': r'10.54.134.158'}
    
    if chosen_family == 'UNI1 Novi Sad' or chosen_family == 'UNI2 Novi Sad':
        table_relative_path = ["Emdep-2", "WTRViewer"]
    else:
        table_relative_path = ["Emdep-2", "WTRViewer", "bin"]

    test_table = os.path.join(home_dir_dict[chosen_family], *table_relative_path)
    ip_to_check = table_ip[chosen_family]


    check_if_online = ping(ip_to_check)
    date_value = check_date_format(datum)
    fyon_value =check_fyon_format(fyon, whole_day)


    if check_if_online:
        if fyon_value and date_value:
            return test_table
        else:
            return None
    else:
        messagebox.showinfo("Error", "Racunar je Offline")


#Proverava da li je datum odgovarajuceg formata i vraca 1 ako jeste, inace raise-uje error i vraca 0.
def check_date_format(input):
    format = '%Y-%m-%d'
    try:
        bool(datetime.datetime.strptime(input, format))
    except ValueError:
        messagebox.showinfo("Error", "Nije unet dobar format za datum")
        return 0
    else:
        return 1


#Proverava da li je fyon odgovarajuceg formata ako jeste vraca 1, takodje ako je stiklirano log za citav dan automatski vraca 1, inace raise-uje error i vraca 0.
def check_fyon_format(input, checkbutton_state):
    if checkbutton_state == 1:
        return 1
    else:
        if len(input) !=9:
            messagebox.showinfo("Error", "Nije unet FYON ili je neodgovarajuceg formata")
            return 0
        else:
            return 1

#Vraca tacnu lokaciju wtr file odnosno DB koju treba obraditi, na osnovu argumenta find_date odnosno datuma kada je snop testiran.
def find_exact_wtr(wtr_folder, find_date):

    datum2 = datetime.date.fromisoformat(find_date)
    file_list_on_path = os.listdir(path=wtr_folder)
    dict_values = {}

    for i in file_list_on_path:
        if i[-3::] == 'mdb':
            full_path = os.path.join(wtr_folder, i)
            date = os.path.getmtime(full_path)
            human_readable_date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')
            dict_values[i] = datetime.date.fromisoformat(human_readable_date)

    dict_values = dict(sorted(dict_values.items(), key=lambda item: item[1]))

    wanted_file = None
    for test in dict_values:
        #print(dict_values[test])
        if dict_values[test] > datum2:
            wanted_file = test
            break

    #print("Unet datum: ", datum2)


    if wanted_file:
        wtr_location = f'{wtr_folder}\\{wanted_file}'
        return wtr_location
    else:
        messagebox.showinfo("Error", "Datum ne sme biti visi ili jedan sa danasnjim!")


#Cita podatke iz DB prema zadatim parametrima i nad tim podacima vrsi serializaciju podataka u file data.pkl
#Pise u file columns.txt kolone iz DB
def export_data_from_db(datum, wtr, fyon, familyy):

    location_to_store_wtr_localy = r'E:\Python\LoggerV2\Files' ###OBRATU PAZNJU!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    if familyy == 'UNI1 Novi Sad' or familyy == 'UNI1 Novi Sad':
        name_of_wtr = wtr.split("\\")[6]
    else:
        name_of_wtr = wtr.split("\\")[7]

    shutil.copy(wtr, location_to_store_wtr_localy)
    end_location = f'{location_to_store_wtr_localy}\\{name_of_wtr}'


    attr1 = datum
    attr2 = end_location
    attr3 = fyon
    subprocess.run([r"E:\Python\LoggerV2\32_bit\.venv\Scripts\python.exe", r"E:\Python\LoggerV2\read_32bit_DB.py", attr1, attr2, attr3])

    os.remove(f"{end_location}")


#Cita fajl columns.txt gde su skladistene kolone DB.
#Cita fajl data.pkl i vrsi deserializaciju podataka.
#Pise deserializovane podatke u excel.
def export_data_to_excel(fyon):

    file = open(r"E:\Python\LoggerV2\Files\columns.txt", mode="r")
    read_data = file.read()
    file.close()
    data_columns = read_data.split(",")


    with open(r"E:\Python\LoggerV2\Files\data.pkl", mode="rb") as file:
        data = pickle.load(file)


    try:
        # store_log_location = fr"E:\Log_Output\output.xlsx"
        store_log_location = fr"E:\Log_Output\{fyon}.xlsx".format(fyon=fyon)
        excel_data = pd.DataFrame(np.array(data), columns = data_columns)
        excel_data.to_excel(store_log_location, index=False)
        messagebox.showinfo("Info", "Uspesno izvadjen log file")
    except Exception as e:
        if data:
            print(e)
        else:
            if fyon == "fyon":
                messagebox.showinfo("Error", "Verovatno se radi o neradnom danu!")
            else:
                messagebox.showinfo("Error", "Trazeni Fyon nije pronadjen")
