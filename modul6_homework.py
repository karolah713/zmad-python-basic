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

#ZADANIE 5
'''Napisz funkcję:
-parametr wejściowy to lista stringów z nazwiskami
-funkcja zapisuje do dwóch oddzielnych plików o nazwach ‘A-M_nazwiska.txt’ oraz ‘N-Ż_nazwiska.txt’ 
odpowiednie nazwiska z podanej listy'''

def sort_names(name_list):
    a_m_names = 'A-M_nazwiska.txt'
    n_ż_names = 'N-Ż_nazwiska.txt'

    with open(a_m_names, 'w', encoding='utf-8') as target_a_n, open(n_ż_names, 'w', encoding='utf-8') as target_n_ż:
        for item in last_names:
            if item[0].lower() in 'aąbcćdeęfghijklłm':
                target_a_n.write(item)
                target_a_n.write('\n')
            if item[0].lower() in 'noóprsśtuvwxyzźż':
                target_n_ż.write(item)
                target_n_ż.write('\n')

last_names = ['Adamczyk', 'Cyd', 'Folk', 'Kowalski','Nalewak', 'Wrona', 'Zorro']
#sort_names(last_names)

###############################################################################################################################

#ZADANIE 6
'''Napisz funkcję, która wyświetla podany tekst odwracając kolejność liter w wyrazach. 
Np. „Ala ma kota” wyświetli „alA am atok”'''

def reversed_words(text):
    text_reversed = ''
    l = (text.split(' '))
    for item in l:
        item_rversed = item[::-1]
        text_reversed += (item_rversed+' ')
    return text_reversed

text = 'Ala ma kota'
#print(reversed_words(text))

###############################################################################################################################

#ZADANIE 7
'''Napisz funkcję, która:
-jako parametr wejściowy pobiera zdanie wpisywane z klawiatury,
-ponownie z klawiatury pobiera nazwę pliku, w którym zapisany zostanie wynik działania funkcji,
-do pliku zapisywane są unikalne wyrazy ze zdania pisane małymi literami po jednym w linii,
-ze zdania zostaną usunięte ewentualne przecinki i kropki.'''

def exc7(sentence):
    input_file_name = input('Please provide the file name: ')
    file_name = input_file_name + '.csv'
    print(file_name)
    l = (sentence.split(' '))
    print(l)

    with open(file_name, 'w', encoding='utf-8') as target:
        for elem in l:
            target.write(elem)
            target.write('\n')

#sentence = input('Please provide a sentence: \n').replace(',','').replace('.','').replace(';','')
#exc7(sentence)
            
###############################################################################################################################

#ZADANIE 8
'''Napisz funkcję, która losuje 5 liczb całkowitych z przedziału <1, 20> dopóki w jednym 
losowaniu nie wystąpi 1 i 20. Wyświetl ilość wykonanych losowań po spełnieniu warunku.'''

def number_finder():
    is_on = True
    n = 1
    numbers = []
    while is_on:
        for draw in range (5):
            num = random.randint(1,20)
            numbers.append(num)
        if 1 in numbers and 20 in numbers:
            is_on = False
        else:
            numbers = []
            n += 1
    return n

#print(number_finder()) 
           
###############################################################################################################################

#ZADANIE 9

'''Napisz funkcję, która posiada zaszytą listę 3 nagród ['samochód', '10000 PLN', 'PS 4 Pro']. 
Przygotuj plik z 10 imionami i nazwiskami zapisanymi po 1 w wierszu. 
Następnie funkcja wczytuje plik, losuje zwycięzcę dla każdej z trzech nagród i zapisuje wyniki 
w pliku o nazwie zwycięzcy.txt wpis postaci: Imię nazwisko, nagroda.'''

def lotery():
    awards = ['samochód', '10000 PLN', 'PS 4 Pro']
    target_file = 'zwyciezcy.txt'
    lotery_names = []
    with open('lotery_names.txt', 'r', encoding='utf-8') as f:
        for name in f:
            lotery_names.append(name.strip())
    with open(target_file, 'w', encoding='utf-8') as target:
        for award in awards:
            name_drawn = random.choice(lotery_names)
            lotery_names.remove(name_drawn)
            target.write(f'{name_drawn}, {award}\n')

lotery()

###############################################################################################################################
            
