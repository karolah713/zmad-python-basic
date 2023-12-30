import csv
from datetime import datetime
import random

###############################################################################################################################
#ZADANIE 1
''' 
Wczytaj plik zamowienia.csv i dokonaj w nim kilku przekształceń:
- pozbądź się znaku z (właściwie zł) z kolumny Utarg
- zamień separator wartości dziesiętnej w tej samej kolumnie na '.'
- pozbądź się spacji jako separatora tysięcy w kolumnie Utarg
- zamień format daty w pliku na RRRR-MM-DD
- Podziel plik na dwie części i zapisz je tak, aby dane dla każdego kraju (Polska, Niemcy) znajdowały się w oddzielnych plikach o nazwach 
zamowienia_polska.csv i zamowienia_niemcy.csv.
'''

def cleanUp_orders():
    dataSource = 'zamowienia.csv'
    dataTarget_Poland = 'zamowienia_polska.csv'
    dataTarget_Germany = 'zamowienia_niemcy.csv'

    with open(dataSource) as source, open(dataTarget_Poland,'w', newline='') as targetP, open(dataTarget_Germany,'w', newline='') as targetG:
        col = ['Kraj', 'Sprzedawca', 'Data zamowienia', 'idZamowienia', 'Utarg']

        reader = csv.DictReader(source, delimiter=";", quotechar='"')
        writerP = csv.DictWriter(targetP, delimiter=';',fieldnames=col)
        writerG = csv.DictWriter(targetG, delimiter=';', fieldnames=col)

        writerP.writeheader()
        writerG.writeheader()

        for row in reader:
            #row['Utarg'] = row['Utarg'].replace('zďż˝', '')
            row['Utarg'] = row['Utarg'].replace(',', '.')
            row['Utarg'] = row['Utarg'].replace(' ', '')
            row['Utarg'] = row['Utarg'][:-4]
            row['Data zamowienia'] = datetime.strptime(row['Data zamowienia'], "%d.%m.%Y").strftime("%Y-%m-%d")

            if row['Kraj'] == 'Polska':
                writerP.writerow(row)
            else:
                writerG.writerow(row)
#cleanUp_orders()

#VERSION 2 (using pandas)

import pandas as pd
def cleanUp_orders2():
    order_data = pd.read_csv('zamowienia.csv', sep=';')

    order_data['Utarg'] = order_data['Utarg'].str.strip('z�')
    order_data['Utarg'] = order_data['Utarg'].replace({',': '.',' ':''}, regex=True)
    order_data['Data zamowienia'] = pd.to_datetime(order_data['Data zamowienia'], dayfirst=True)

    order_data[order_data.Kraj == 'Polska'].to_csv('zamowienia_polska2.csv', index=False)
    order_data[order_data.Kraj == 'Niemcy'].to_csv('zamowienia_niemcy2.csv', index=False)

#cleanUp_orders2()

###############################################################################################################################

#ZADANIE 2
'''Napisz funkcję, która przyjmuje listę plików oraz nazwę nowego pliku jako argumenty wejściowe. 
Funkcja scala zawartość plików w jeden plik wynikowy o podanej wcześniej nazwie.'''

def create_bulk_file(bulkFileName, *args):
    col = ['Kraj', 'Sprzedawca', 'Data zamowienia', 'idZamowienia', 'Utarg']
    with open(bulkFileName, 'w', newline='') as target:
        writer = csv.DictWriter(target, delimiter=';', fieldnames=col)
        writer.writeheader()
        for arg in args:
            with open(arg) as source:
                reader = csv.DictReader(source, delimiter=";", quotechar='"')
                for row in reader:
                    writer.writerow(row)

#create_bulk_file('zamowienia_all.csv','zamowienia_polska.csv','zamowienia_niemcy.csv')

#VERSION 2 (using pandas)
                                 
def create_bulk_file2(bulkFileName, *args):
    df = pd.DataFrame(args)

    files_list = df[0].values.tolist()

    concatenated_list = (pd.read_csv(f) for f in files_list)
    concatenated_df = pd.concat(concatenated_list, ignore_index=True)
    concatenated_df.to_csv(bulkFileName, index=False)

#create_bulk_file2('zamowienia_all2.csv','zamowienia_polska2.csv','zamowienia_niemcy2.csv')

###############################################################################################################################

#ZADANIA POWTÓRZENIOWE

#ZADANIE 3
'''Napisz funkcję, która będzie zwracała 3 największe wartości z listy numerycznej. 
Lista jest parametrem wejściowym funkcji.'''

def return_3max(numeric_list):
    max_3_num = []
    for _ in range(3):
        max_number = max(numeric_list)
        max_3_num.append(max_number)
        numeric_list.remove(max_number)
    return max_3_num

#print(return_3max([1,2,3,6,8,100,87]))

###############################################################################################################################

#ZADANIE 4
'''Mając listę mieszana = [1, 2.3, ‘Zbyszek’, 5, ‘Marian’, 3.0] napisz funkcję, 
która zapisze wartości dla każdego typu do słownika gdzie pod kluczem równym nazwie typu 
zmiennej (int, float, str, itp.) wartością będzie lista elementów z listy 'mieszana' danego typu. 
Przykład: {'int': [1,5], 'str': ['Zbyszek','Marian']} itd.'''

mieszana = [1, 2.3, "Zbyszek", 5, "Marian", 3.0]
def create_type_dict(list):
    type_dict = {'int':[], 'str':[], 'float':[]}
    for elem in mieszana:
        if type(elem) == int:
            type_dict['int'].append(elem)
        if type(elem) == str:
            type_dict['str'].append(elem)
        if type(elem) == float:
            type_dict['float'].append(elem)
    return type_dict

#print(create_type_dict(mieszana))

###############################################################################################################################