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

create_bulk_file2('zamowienia_all2.csv','zamowienia_polska2.csv','zamowienia_niemcy2.csv')

###############################################################################################################################