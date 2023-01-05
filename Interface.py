import tkinter as tk
from time import sleep

from Class import *
from Functions import * 

# Classe mun
class Interface:

    def __init__(self):
        # Constructeur de la fenetre principale
        self.root = tk.Tk()
        self.root.geometry("300x500")
        
        self.orderBook = LimitOrderBook()
        self.Orders = LimitOrderBook()
        self.history = History()
        # Instanciation du Menu
        self.Menu()

        self.root.mainloop()

    # Fonction qui permet la creation de plusieurs Label + Entry sur l'interface
    def Create_Entry(self,Text):
        l = []
        e = []
        variables = {}
        for i in range(0,len(Text)):
            l.append(tk.Label(self.root,text = Text[i], height=4).grid(row=i, column=0))
            variables[i] = tk.StringVar()
            e.append(tk.Entry(self.root,textvariable=variables[i], width=20).grid(row=i, column=1))
   
        self.label = l
        self.entry = e
        self.entry_get = variables

    # Permet d'afficher label + entry
    def Post_Entry(self):
        for i in range(0,len(self.label)):
            self.label[i]
            self.entry[i]

    def PopUp_Exception(self):
        self.f = tk.Tk()
        self.f.title('Exceptions')
        self.f.geometry("250x40")
        label = tk.Label(self.f, text="\nERROR INPUTS FORMAT !!")
        label.pack()
        self.f.mainloop()


    # Permet de gerer les exceptions dans l'entrée des données si c'est un int et si sup à 0
    def Menu_Exception(self):
        co = 0
        for i in range(0,len(self.entry_get)):
            try :
                if isinstance(int(self.entry_get[i].get()), int) and int(self.entry_get[i].get())>0:
                    co += 1
            except:
                self.PopUp_Exception()
                self.f.destroy()


        if co == len(self.entry_get):
            self.Gestion_Algo()
        else:
            self.PopUp_Exception()
            self.f.destroy()

    # Permet dee lancer l'ensemble des fonctions de Functions.py et d'instancier les classes de Class.py
    def Gestion_Algo(self):
        # Initialisation des variables
        self.vars = []
        for i in range(0,len(self.entry_get)):
            self.vars.append(int(self.entry_get[i].get()))
        
        # On reinitialise les fichiers excel
        # overwrite()

        # Initalisation d'un order book
        self.orderBook.GenerateRandom_OrderBook(self.vars[0], self.vars[1], self.vars[2], self.vars[3], self.vars[4], "no")

        # Creation de plusieurs ordres aléatoires
        self.Orders.GenerateRandom_OrderBook(self.vars[5], self.orderBook.Price_Mean(), self.vars[2], self.vars[3], self.vars[4], "yes")

        # Entré des nouveaux ordres créé sur le marché 
        self.orderBook, self.history = match_orderBook_orders(self.orderBook, self.Orders.orders, self.history)

        # Print outstanding et orderboook
        self.orderBook.Outstanding()
        self.orderBook.Sort_Price(self.orderBook.Price_Mean())
        print(self.orderBook)


    # Menu premier page
    def Menu(self):
        self.root.title('Menu')
        
        Text = ["Nombre limitOrder : ","Prix départ : ", "Standart Deviation du prix : ",
        "Quantité Moyenne : ", "Quantité Standart Deviation : ", "Nombre d'ordres : "]
        # Mise en place du menu sous forme de Label et Entry
        self.Create_Entry(Text)
        self.Post_Entry()

        # Creation d'un button afin de récupérer les résultats
        tk.Button(self.root, text = "Submit",
        command = lambda : self.Menu_Exception(),
        fg='White', bg= 'dark green').grid(row=len(self.label),column=1)

        tk.Button(self.root, text="Quit", command=self.root.destroy,
        fg='White', bg= 'red').grid(row=len(self.label)+2,column=1)

        # Pour que l'action enter fonctionne
        # self.root.bind('<Return>',lambda event:self.Menu_Exception())


