import datetime
import sys
import pickle
import pyodbc

def process_db(datum01, wtr, fyon):

    columns = []
    input_date_splitted = datum01.split('-')
    lista = ['10', '20', '30']
    input_date_int = []
    for i in input_date_splitted:
        if i in lista:
            input_date_int.append(eval(i))
        else:
            input_date_int.append(eval(i.strip("0")))

    datum1 = datetime.datetime(*input_date_int)
    datum2 = datum1 + datetime.timedelta(days=1)


    connection_string = (r'DRIVER={Microsoft Access Driver (*.mdb)};'
                         fr'DBQ={wtr};')
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    if fyon == "None":
        data = cursor.execute("select * from SolvedErrors where DateBegin > ? and DateBegin < ?", datum1, datum2).fetchall()
    else:
        data = cursor.execute("select * from SolvedErrors where Ref = ?", fyon).fetchall()

    for i, _ in enumerate(cursor.description):
        columns.append(cursor.description[i][0])

    file = open(r"E:\Python\LoggerV2\Files\columns.txt", mode="w")
    for number, i in enumerate(columns):
        if number == len(columns) - 1:
            file.write(i)
        else:
            file.write(f'{i},')
    file.close()

    cursor.close()
    connection.close()

    with open(r"E:\Python\LoggerV2\Files\data.pkl", mode="wb") as file:
        pickle.dump(data, file)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python my_script.py <attr1>, <attr2>, <attr3>")
        sys.exit(1)

    attribute1 = sys.argv[1]
    attribute2 = sys.argv[2]
    attribute3 = sys.argv[3]
    process_db(attribute1, attribute2, attribute3)
