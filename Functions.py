from Class import *
from File import *
from time import sleep


    

# Fonction qui permet de calculer la difference de quantite entre l'ordre et le limitOrder
def match_order_Operation(order, limit_order, limitOrderBook, history, id_remove, compt):
    # Si la quantité de l'ordre est strictement superieur alors il faut soustraire sa quantite
    # Créer une operation a mettre dans l'historique
    if order.quantity > limit_order.quantity:
        id_remove.append(limit_order.order_id)
        history.add_history(order,limit_order,limitOrderBook, id_remove)
        order.quantity = order.quantity - limit_order.quantity     
    
    # Si la quantité de l'ordre est egal a la quantite du limit order
    # Ajoute l'operation dans l'historique
    # Remove le limit order de l'orderbook
    elif order.quantity == limit_order.quantity:
        id_remove.append(limit_order.order_id)
        history.add_history(order, limit_order, limitOrderBook, id_remove)
        limitOrderBook.remove_orderMultiple(id_remove)
        compt=1

    # Si la quantité de l'ordre est inférieur a la quantite du limit order
    # Ajoute dans l'historique 
    # Enleve la quantite du limit order 
    else:
        history.add_history(order, limit_order, limitOrderBook, id_remove)
        limit_order.quantity = limit_order.quantity - order.quantity
        limitOrderBook.remove_orderMultiple(id_remove)
        compt=1

    return limitOrderBook, history, compt, id_remove

# Permet de procéder à la gestion d'un nouvel ordre sur le marché (orderbook)
def match_order_limitMarket(order, limitOrderBook, history):
    # Creation d'une variable afin de récolter les order_id à supprimer
    id_remove = []
    compt=0
    for limit_order in limitOrderBook.orders :
        # Permet de verifier si l'ordre passé en parametre ne touche pas un autre ordre present l'orderbook
        if order.direction != limit_order.direction :
            # Cette condition permet de verifier si l order de type LimitOrder 
            # Autres conditions : flemme
            # Permet de rentrer et de faire les calculs necessaires
            if isinstance(order, LimitOrder) and ((order.price >= limit_order.price and order.direction == "buy") or (order.price <= limit_order.price and order.direction == "sell")):
                limitOrderBook, history, compt, id_remove = match_order_Operation(order, limit_order, limitOrderBook, history, id_remove, compt)
                
            # On break car etant donné qu'avec la boucle on parcours l'orderbook qui est classé par montant,
            # le premier qui apparait et dont le prix ne correspond pas au prix entré dans l'ordre,
            # alors il ne touchera aucun autre ordre
            elif isinstance(order, MarketOrder):
                limitOrderBook, history, compt, id_remove = match_order_Operation(order, limit_order, limitOrderBook, history, id_remove, compt)
            else:
                limitOrderBook.add_order(order)
                limitOrderBook.remove_orderMultiple(id_remove)
                sleep(0.005)
                return limitOrderBook, history
        # si compt == 1 c'est à dire qu'il faut sortir de la boucle car l'order a été fill
        if compt == 1:
            return limitOrderBook, history

    # Gestion de l'exception si le market order ou le limit order fill tous les autres ordres
    # Gestion de l'exception quand l'order fill entierement l'orderbook
    # Reinitialise le prix au dernier prix achete (Securite pour eviter qu'un prix tombe à 0)
    if isinstance(order, MarketOrder):
        order = LimitOrder(order.direction,limitOrderBook.orders[len(id_remove)-1].price,order.quantity)
    elif isinstance(order, LimitOrder):
        order.price = limitOrderBook.orders[len(id_remove)-1].price
        
    # Ajout de l'order dans l'orderbook
    limitOrderBook.add_order(order)
    limitOrderBook.remove_orderMultiple(id_remove)
            
    return limitOrderBook, history

# Fonction qui initalise toute les foncitons pour tout nouveau ordre sur le marché en gérant les
def match_order(order, limitOrderBook, history):
    if isinstance(limitOrderBook, LimitOrderBook) and isinstance(history, History):
        if isinstance(order, LimitOrder) or isinstance(order, MarketOrder):
            # Permet d'avoir le temps comme premier tri ce qui pourra faire fill en fonction du temps si deux ordres ont le même prix
            limitOrderBook.orders = sorted(limitOrderBook.orders,key=lambda x: x.submitted_time)
            match order.direction:
                case "buy":
                    limitOrderBook.orders = sorted(limitOrderBook.orders,key=lambda x: x.price)
                    limitOrderBook.orders = sorted(limitOrderBook.orders,key=lambda x: x.direction, reverse=True)
                    limitOrderBook, history = match_order_limitMarket(order,limitOrderBook, history)
                    sleep(0.000000001)
                    return limitOrderBook, history
                case "sell":
                    # Pour sell on va juste inversé le sorted afin que celui ci soit dans le decroissant et commence par les sell
                    limitOrderBook.orders = sorted(limitOrderBook.orders,key=lambda x: x.price, reverse=True)
                    limitOrderBook.orders = sorted(limitOrderBook.orders,key=lambda x: x.direction)
                    limitOrderBook, history = match_order_limitMarket(order,limitOrderBook, history)
                    sleep(0.000000001)
                    return limitOrderBook, history                    
                # Exception au cas la direction ne correspondrait pas à buy ou sell
                case _:
                    print("Wrong direction")
                    return limitOrderBook, history

        # Exception au cas order n'est pas du bon type
        else:
            print("Invalid order type")
            return limitOrderBook, history
    else:
        print("Wrong orderbook or history types")
        return limitOrderBook, history

# Fonction qui permet de fusionner un orderbook existant à une série d'ordre
def match_orderBook_orders(orderBook, orders, history):
    for order in orders:
        add_excelSpread(orderBook)
        orderBook, history = match_order(order,orderBook,history)
    return orderBook, history