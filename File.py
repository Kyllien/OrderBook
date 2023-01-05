import datetime
import pandas as pd
import numpy as np
import os
import openpyxl
from Class import *

# Add the trade in History.txt 
def add_txt(Ope):
    with open("Sortie/History.txt",'a',encoding = 'utf-8') as f:
        f.write(str(Ope))
        f.close()

# Overwrite the 2 sheets 
def overwrite(l = ['Sortie/History_Price.xlsx','Sortie/History_Spread.xlsx','Sortie/History_Price_default.xlsx','Sortie/History_Spread_default.xlsx']):
    for i in range(0,int(len(l)/2)):
        # Exception si le fichier à supprimer n'existe pas
        if os.path.isfile(l[i]):
            os.remove(l[i])
        else:
            print("le fichier " + l[i] + " est inexistant, mais pas grave il va être créé")

        # Exception si le dossier defaut n'existe pas
        try :
            df = pd.read_excel(l[i + int(len(l)/2)])
            if l[i].find("Price"):
                df.to_excel(l[i])
            else:
                df.to_excel(l[i])

            
        except FileExistsError:
            print("T'abuses")
            exit()
    
    

# Add the trade in History_Price.xlsx
def add_excelPrice(limitOrder):
    df1 = pd.read_excel("Sortie/History_Price.xlsx")
    df2 = pd.DataFrame(np.array([[float(limitOrder.price),datetime.datetime.today()]]), columns=['Price','Time'])
    df3 = pd.concat([df1[["Price","Time"]],df2])
    # Append DataFrame to existing excel file
    df3[['Price','Time']].to_excel("Sortie/History_Price.xlsx")

# Add the spread in History_Spread.xlsx
def add_excelSpread(orderBook):
    spread = orderBook.compute_bid_ask_spread()
    df1 = pd.read_excel("Sortie/History_Spread.xlsx")
    df2 = pd.DataFrame(np.array([[spread,datetime.datetime.today()]]), columns=['Spread','Time'])
    df3 = pd.concat([df1[["Spread","Time"]],df2])
    # Append DataFrame to existing excel file
    df3[['Spread','Time']].to_excel("Sortie/History_Spread.xlsx")