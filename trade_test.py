


class Offer:
    def __init__(self, amount, price, seller):
        self.amount = amount 
        self.price = price
        self.seller = seller

    def __str__(self):
    	return "Agent " + str(self.seller) + ": sell " + str(self.amount) + " shares @" + str(self.price)
        
class Demand:
    def __init__(self, amount, price, buyer):
        self.amount = amount
        self.price = price
        self.buyer = buyer

    def __str__(self):
    	return "Agent " + str(self.buyer) + ": buy " + str(self.amount) + " shares @" + str(self.price)


# assume there is only 1 stock

 # offer & demand: 
    # type: list
    # description: agents' orders
# state:
    # type: dictionary
    # description: key is the agent ID, and value is a list, [cash, stock holdings]
    #			ID: [cash, stock]
def trade(state, offers, demands):
    # sort offer list in acensding order
    offers.sort(key=lambda x:x.price)
    # sort demand list in descending order
    demands.sort(key=lambda x:x.price, reverse=True)
    offer_pointer = 0
    demand_pointer = 0
    while offer_pointer < len(offers) and demand_pointer < len(demands):
        # in favor of buyers when bid price is greater than offer
        if offers[offer_pointer].price <= demands[demand_pointer].price:
            if offers[offer_pointer].amount >= demands[demand_pointer].amount:

                amt_change = demands[demand_pointer].amount
                cash_change = offers[offer_pointer].price * amt_change

                # ensure Agent has sufficient stocks to sell
                if amt_change > state[offers[offer_pointer].seller][1]:
                	print()
                	raise Exception("Agent "+ str(offers[offer_pointer].seller) + " doens't have sufficient stock to sell")

                # ensure Agent has enough money to buy
                if cash_change > state[demands[demand_pointer].buyer][0]:
                	raise Exception("Agent "+ str(offers[offer_pointer].seller)+ " doens't have enough money to buy")

                # change cash 
                state[offers[offer_pointer].seller][0] += cash_change
                state[demands[demand_pointer].buyer][0] -= cash_change
                # change stock holdings
                state[offers[offer_pointer].seller][1] -= amt_change
                state[demands[demand_pointer].buyer][1] += amt_change

                # change shares filled & unfilled
                offers[offer_pointer].amount -= amt_change
                demands[demand_pointer].amount -= amt_change

                # increment indices
                if offers[offer_pointer].amount == demands[demand_pointer].amount:
                    offer_pointer += 1
                demand_pointer += 1

            else:

                amt_change = offers[offer_pointer].amount
                cash_change = offers[offer_pointer].price * amt_change

                # ensure Agent has sufficient stocks to sell
                if amt_change > state[offers[offer_pointer].seller][1]:
                	print()
                	raise Exception("Agent "+ str(offers[offer_pointer].seller) + " doens't have sufficient stock to sell")

                # ensure Agent has enough money to buy
                if cash_change > state[demands[demand_pointer].buyer][0]:
                	raise Exception("Agent "+ str(offers[offer_pointer].seller)+ " doens't have enough money to buy")

                # change cash
                state[offers[offer_pointer].seller][0] += cash_change
                state[demands[demand_pointer].buyer][0] -= cash_change
                # change stock holdings
                state[offers[offer_pointer].seller][1] -= amt_change
                state[demands[demand_pointer].buyer][1] += amt_change

                # change shares filled & unfilled
                demands[offer_pointer].amount -= amt_change
                offers[offer_pointer].amount -= amt_change

                # increment index
                offer_pointer += 1
        else:
        	break


def main():
	state = {}
	state[1] = [100, 0]
	state[2] = [50,10]
	state[3] = [20, 20]
	state[4] = [80, 5]
	print(state)

	offers = [Offer(10, 12, 2), Offer(20, 15, 3)]
	demands = [Demand(10, 12, 1), Demand(12, 5, 4)]


	for x in offers:
		print(x)
	for x in demands:
		print(x)

	trade(state, offers, demands)

	print(state)
	for x in offers:
		print(x)
	for x in demands:
		print(x)

main()






