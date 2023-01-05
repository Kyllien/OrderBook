import datetime
import random
import itertools
from time import sleep

from File import *

class LimitOrder: 
    id_LimitOrder = itertools.count()

    def __init__(self, direction, price, quantity): 
        self.order_id = next(LimitOrder.id_LimitOrder)
        self.direction = direction 
        self.price = float("{:.2f}".format(price))
        self.quantity = int(quantity)
        self.submitted_time = datetime.datetime.today()

    def __str__(self):
        return f"id : {self.order_id}, direction : {self.direction}, price : {self.price}, quantity : {self.quantity}, date : {self.submitted_time}\n"

class MarketOrder: 
    id_MarketOrder = itertools.count()

    def __init__(self, direction, quantity): 
        self.direction = direction 
        self.quantity = int(quantity)
        self.submitted_time = datetime.datetime.today()
        self.order_id = next(MarketOrder.id_MarketOrder)

    def value(self,value):
        self.price = value

    def __str__(self):
        return f"Id : {self.order_id}, direction : {self.direction}, quantity : {self.quantity}, submitted_time : {self.submitted_time}\n"

class Operation:
    id_Operation = itertools.count()

    def __init__(self, marketOrder, limitOrder):
        self.ope_id = next(Operation.id_Operation)
        self.time = datetime.datetime.today()
        self.marketOrder = marketOrder
        self.limitOrder = limitOrder

    def __str__(self):
        return f"Id : {self.ope_id}\nOrder : {self.marketOrder}limitOrder : {self.limitOrder}time : {self.time} \n"
        
class History:
    def __init__(self):
        self.operations = []
    
    def add_history(self, marketOrder, limitOrder, orderBook, id_remove):
        Ope = Operation(marketOrder, limitOrder)
        self.operations.append(Ope)
        self.operations = sorted(self.operations, key=lambda x: x.time)
 
        add_txt(Ope)
        add_excelPrice(limitOrder)


    def __str__(self):
        text = ""
        for operation in self.operations:
            text = text + f"{operation}"
        return  text

class LimitOrderBook: 
    def __init__(self): 
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def remove_order(self, order_id):
        for order in self.orders:
            if order.order_id == order_id:
                self.orders.remove(order)
                break

    def remove_orderMultiple(self,id_remove):
        # Suppression des limit order qui ont été fill afin d'éviter des problemes avec la boucle for et la suppression
        for id in id_remove:
            self.remove_order(id)
        self.orders = sorted(self.orders, key=lambda x: x.price)

    def __str__(self):
        text = ""
        for order in self.orders:
            text = text + f"{order}"
        return text

    # Fonction qui crée aléatoirement un limit order 
    def GenerateRandom_LimitOrder(self,Input_Price,Input_SigmaPrice, quantity):
        price = random.gauss(Input_Price,Input_SigmaPrice)
        # Test si price ou qty sont negatif recommence jusqu'à qu'ils soient ok
        while(price <= 0 ):
            price = random.gauss(Input_Price,Input_SigmaPrice)

        # En fonction du prix ca donne la direction :  buy si prix > 100 
        if price <= Input_Price:
            direction = "buy"
        else:
            direction = "sell"
        order = LimitOrder(direction, price, quantity)               
        self.add_order(order)

    # Créer un orderbook aléatoirement en fonction des parametres transmis
    def GenerateRandom_OrderBook(self, Input_Nb, Input_Price, Input_SigmaPrice, Input_Qty, Input_SigmaQty, Market):
        # Si c'est pour intialiser un order book : que des limit order
        if Market == "no":
            for i in range(0,Input_Nb):
                sleep(0.000000001)
                # Creer une quantite aleatoire
                quantity = random.gauss(Input_Qty, Input_SigmaQty)
                while(quantity <= 0 ):
                    quantity = random.gauss(Input_Qty, Input_SigmaQty)
                #Add LimitOrder
                self.GenerateRandom_LimitOrder(Input_Price,Input_SigmaPrice, quantity)
        # Si c'est pour initialiser une serie aléatoire d'ordre  
        elif Market == "yes":
            for i in range(0,Input_Nb):
                sleep(0.00000001)
                # Choisis aleatoirement si c'est un market order ou un limit order
                ch = random.choice(["Limit","Market"])
                quantity = random.gauss(Input_Qty, Input_SigmaQty)
                while(quantity <= 0 ):
                    quantity = random.gauss(Input_Qty, Input_SigmaQty)
                
                # Si choix est Limit order ou Marketorder
                if ch == "Limit":
                    self.GenerateRandom_LimitOrder(Input_Price,Input_SigmaPrice, quantity)
                else:
                    direction = random.choice(["buy","sell"])
                    order = MarketOrder(direction,quantity)
                    self.add_order(order)
        else:
            print("Market not ok")

    # Permet de récupérer les 10 limitOrder "buy" et "sell" qui sont le plus proche de fill
    def Outstanding(self):
        # Trie de facon à ceux que les 10 premiers de la liste soit ceux que nous cherchons
        self.orders = sorted(self.orders, key=lambda x: x.price,reverse=True)
        self.orders = sorted(self.orders, key=lambda x: x.direction)
        # Boucle for pour parcourir les 10 premiers buy et les print
        print("10 outstandings 'buy' : \n")
        for i in range(0,10):
            print(self.orders[i])

        # Trie de facon à ceux que les 10 premiers de la liste soit ceux que nous cherchons
        self.orders = sorted(self.orders, key=lambda x: x.price)
        self.orders = sorted(self.orders, key=lambda x: x.direction,reverse=True)
        # Boucle for pour parcourir les 10 premiers sell et les print
        print("10 outstandings 'sell' : \n")
        for i in range(0,10):
            print(self.orders[i])
    
    # Permet d'avoir la difference en absolut et donc d'avoir l'ecart entre chaque buy et sell, et le prix moyen
    def closest_to_target(cls,order_price, price):
        return abs(order_price - price)

    # Permet de trier l'orderbook en fonction des prix qui sont le plus proches d'etre fill
    def Sort_Price(self, price):
        self.orders = sorted(self.orders, key=lambda x: self.closest_to_target(x.price,price))

    # Permet de faire la moyenne des prix pour classer mais aussi pour la creation de nouveaux random
    def Price_Mean(self):
        l = []
        for i in self.orders:
            l.append(i.price)
        return sum(l)/len(l)

    # Permet de calculer spread bid ask
    def compute_bid_ask_spread(self): 

        buy_prices = [order.price for order in self.orders if order.direction == "buy"] 
        sell_prices = [order.price for order in self.orders if order.direction == "sell"] 

        bid = max(buy_prices) 
        ask = min(sell_prices) 
        spread = ask - bid 
        return spread
    

    

    