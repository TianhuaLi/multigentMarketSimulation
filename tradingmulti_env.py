"""
@author: Andjela Mladenovic
Environment for trading game.
February 5th, 2019.
"""
import random
import csv
import pandas
import sys
import math
import numpy as np
import gym
from gym import spaces
from gym.utils import seeding
import gym_tradingmulti.envs.agent as agt

NUM_ROUNDS_PROFIT = 50
MAX_NUM_EPISODES = 100000
agent = agt.HardCodedAgent()
learningAgent = agt.LearningAgent(1)


#HELPFUL CLASSES
class Offer:
    #Offer contains the amount the seller offered to sell for what stocks and for what price. It also contains the index of the seller. 
    def __init__(self, amount, price, seller, stock):
        self.amount = amount 
        self.price = price
        self.seller = seller
        self.stock = stock

    #printing functions
    def print_everything_about_offer(self):
        print("Offer: Agent "+ str(self.seller) +" selling stock " + str(self.stock) + " for the price " + str(self.price) + " and amount " + str(self.amount))
        
class Demand:
    #Demand contains the amount  the buyer offered to buy for what stock and for what price. It also contains index of the buyer.
    def __init__(self, amount, price, buyer, stock):
        self.amount = amount
        self.price = price
        self.buyer = buyer
        self.stock = stock

    #printing functions
    def print_everything_about_demand(self):
        print("Demand: Agent "+ str(self.buyer) + " buying stock " + str(self.stock) + " for the price " + str(self.price) + " and amount " + str(self.amount))

class TradingEnv(gym.Env):
   #HELPFUL FUNCTIONS
    def transaction(self, offers, demands, print_info):
        for i in range(len(demands)):
            trade_happened = False
            point_offer = 0
            point_demand = 0
            while ((point_offer < len(offers[i])) and (point_demand < len(demands[i]))):
                if ((demands[i][point_demand].price >= offers[i][point_offer].price) and (demands[i][point_demand].amount <= offers[i][point_offer].amount)):
                    
                    #changing seller agent
                    self.state[offers[i][point_offer].seller * self.NUM_STOCKS + offers[i][point_offer].stock] = self.state[offers[i][point_offer].seller * self.NUM_STOCKS + offers[i][point_offer].stock] - demands[i][point_demand].amount
                    self.state[offers[i][point_offer].seller + self.NUM_AGENTS * self.NUM_STOCKS] = self.state[offers[i][point_offer].seller + self.NUM_AGENTS * self.NUM_STOCKS] + demands[i][point_demand].amount * offers[i][point_offer].price 
                    
                    #changing buy agent
                    self.state[demands[i][point_demand].buyer * self.NUM_STOCKS + demands[i][point_demand].stock] = self.state[demands[i][point_demand].buyer * self.NUM_STOCKS + demands[i][point_demand].stock] + demands[i][point_demand].amount
                    self.state[demands[i][point_demand].buyer + self.NUM_AGENTS * self.NUM_STOCKS] = self.state[demands[i][point_demand].buyer + self.NUM_AGENTS * self.NUM_STOCKS]- demands[i][point_demand].amount * offers[i][point_offer].price 

                   #Trade is happening fully
                    offers[i][point_offer].amount = offers[i][point_offer].amount - demands[i][point_demand].amount
                    demands[i][point_demand].amount = 0
                    point_demand = point_demand + 1

                elif ((demands[i][point_demand].price >= offers[i][point_offer].price) and (demands[i][point_demand].amount >= offers[i][point_offer].amount)):
                
                    #changing seller agent
                    self.state[offers[i][point_offer].seller * self.NUM_STOCKS + offers[i][point_offer].stock] = self.state[offers[i][point_offer].seller * self.NUM_STOCKS + offers[i][point_offer].stock] - offers[i][point_offer].amount
                    self.state[offers[i][point_offer].seller + self.NUM_AGENTS * self.NUM_STOCKS] = self.state[offers[i][point_offer].seller + self.NUM_AGENTS * self.NUM_STOCKS] + offers[i][point_offer].amount * offers[i][point_offer].price 

                    #changing buy agent
                    self.state[demands[i][point_demand].buyer * self.NUM_STOCKS + demands[i][point_demand].stock] = self.state[demands[i][point_demand].buyer * self.NUM_STOCKS + demands[i][point_demand].stock] + offers[i][point_offer].amount
                    self.state[demands[i][point_demand].buyer + self.NUM_AGENTS * self.NUM_STOCKS] = self.state[demands[i][point_demand].buyer + self.NUM_AGENTS * self.NUM_STOCKS] - offers[i][point_offer].amount * offers[i][point_offer].price 
                    
                    #Trade is happening partially 
                    demands[i][point_demand].amount = demands[i][point_demand].amount - offers[i][point_offer].amount
                    offers[i][point_offer].amount = 0
                    point_offer = point_offer + 1
            
                elif((demands[i][point_demand].price < offers[i][point_offer].price)):
                    #trade is not happening
                    point_demand = point_demand + 1

        if print_info == True:    
            for i in range(len(offers)):
                for j in range(len(offers[i])):
                    offers[i][j].print_everything_about_offer()

            for i in range(len(demands)):
                for j in range(len(demands[i])):
                    demands[i][j].print_everything_about_demand()



    # assume there is only 1 stock

    # offer & demand: 
        # type: list
        # description: agents' orders
    # state:
        # type: dictionary
        # description: key is the agent ID, and value is a list, [cash, stock holdings]
    def trade(self):
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

                    # change cash 
                    self.state[offers[offer_pointer].seller][0] += cash_change
                    self.state[demands[demand_pointer].buyer][0] -= cash_change
                    # change stock holdings
                    self.state[offers[offer_pointer].seller][1] -= amt_change
                    self.state[demands[demand_pointer].buyer][1] += amt_change

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
                    # change cash
                    self.state[offers[offer_pointer].seller][0] += cash_change
                    self.state[demands[demand_pointer].buyer][0] -= cash_change
                    # change stock holdings
                    self.state[offers[offer_pointer].seller][1] -= amt_change
                    self.state[demands[demand_pointer].buyer][1] += amt_change

                    # change shares filled & unfilled
                    demands[offer_pointer].amount -= amt_change
                    offers[offer_pointer].amount -= amt_change

                    # increment index
                    offer_pointer += 1
            else:
                break





    #MAIN FUNCTIONS for the environment - Initialization, step, reset
    def __init__(self):
        #Every env comes with an action-space and observation-space.
        #first we only have one stock (this is inital version, should be working for multiple stocks)
        df_all = pandas.read_csv('data_monthly_20years.csv')
        df = ((df_all['Open']))
        #array_values contain the historical data of the stocks, that will be used as profit
        self.array_values = np.array(df.values)
        self.array_values = self.array_values[~np.isnan(self.array_values)]
        #total number of stocks
        self.NUM_STOCKS = 1
        #total number of agents is = number of learned agents + number of hardcoded agents        
        self.NUM_AGENTS_total = 3 
        #number of learned agents
        self.NUM_AGENTS = 1 
        #starting money of each agent - arbitraty chosen 40 for now
        self.money_start = 40
        #flag when to stop - currently unused
        self.done = False
        #the round of trading
        self.round = 0
        self.profit = 0
        #NUM_AGENTS*NUM_STOCKS is the total number of the elements, it is like array of the tuples (a, b, c)
        #a - the action 1 - buy
        #               2 - sell 
        #               0 - hold
        # b - the amount of the stock bougth/sold (it represents the percentage range: [0..1]
        # c - price the seller is willing to sell for, or buyer to buy for
        self.action_space = spaces.Box(low = np.array([0]*self.NUM_AGENTS*self.NUM_STOCKS*3), high = np.array([2, 1, sys.float_info.max]*self.NUM_AGENTS*self.NUM_STOCKS), dtype=np.float32)
        self.observation_space = spaces.Box(low = np.array([0]*(self.NUM_AGENTS*self.NUM_STOCKS + self.NUM_AGENTS + 5*self.NUM_STOCKS)) , high = np.array([1]*self.NUM_STOCKS*self.NUM_AGENTS + [sys.float_info.max]*(self.NUM_AGENTS + 5*self.NUM_STOCKS)), dtype = np.float32 )
        
        self.seed()
        self.reset()

    #SETTING SEED
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    #STEP FUNCTION - WHERE ACTUAL TRADING HAPPENDS
    def step(self, action):
        self.round = self.round + 1
        self.profit = 1
        #self.profit = self.array_values[self.round - 1]
        self.action_space = np.copy(action)
        #checked if maximum number of episodes reached if yes, terminate
        print_info = False
        if ((abs(action[0] - 1.00) < 0.01) and (action[1] > 0.01) and (action[2] > 0.01)):
            print_info = True
            print("BUYING-------BUYING-------BUYING.")
        if ((abs(action[0] - 2.00) < 0.01) and (action[1] > 0.01)and(action[2]>0.01)):
            print("SELLING-------SELLING-------SELLING")
        if (self.round == MAX_NUM_EPISODES):
            self.done = True
        #FOR NOW WE ONLY HAVE ONE STOCK
        offers = []
        demands = []
        reward = []
        #for bounding moves 
        x = 0
        #Storing all selling offers in "offer" queue and buying offers in "demand" queue
        for j in range(self.NUM_STOCKS):
            offer_stock=[]
            demand_stock=[]
            for i in range(self.NUM_AGENTS):
                #add artifically agents - HARD CODED AGENTS FOR BUYING
                # offer_stock.append(Offer(0.5,0.15,2,j))
                offer_stock.append(agent.get_offer(j))  ########################### modified  ##############################
                #add artifically agents - HARD CODED AGENTS FOR SELLING
                # demand_stock.append(Demand(0.2,0.20,1,j))
                demand_stock.append(agent.get_demand(j)) ########################### modified  ##############################

                # if ((abs(action[3*i*self.NUM_STOCKS + 3*j] - 1.00) < 0.01) and (action[3*i*self.NUM_STOCKS + 3*j + 2] > 0) and (action[3*i*self.NUM_STOCKS + 3*j + 1] > 0)): 
                #     demand_stock.append(Demand(action[3*i*self.NUM_STOCKS + 3*j + 2], action[3*i*self.NUM_STOCKS + 3*j + 1] ,i, j))
                   
                # elif ((abs(action[3*i*self.NUM_STOCKS + 3*j] - 2.00) < 0.01)and (action[3*i*self.NUM_STOCKS + 3*j + 2] > 0) and (action[3*i*self.NUM_STOCKS + 3*j + 1] > 0)): 
                #     offer_stock.append(Offer(action[3*i*self.NUM_STOCKS + 3*j + 2], action[3*i*self.NUM_STOCKS + 3*j + 1] ,i, j))

                ########################### modified  ##############################
             #   learningAgent.take_action(action, i, j, demand_stock, offer_stock)
                    
            offers.append(offer_stock)
            demands.append(demand_stock)
        #sorting offers according to price
        for i in range(len(offers)):
            offers[i].sort(key=lambda x:x.price)
        #sorting demands randomly - which presents the time 
        for i in range(len(demands)):
            random.shuffle(demands[i])
        #print information if print_info true (if the agent learned to buy when profit is positive constant)
        if (print_info == True):
            for i in range(len(offers)):
                for j in range(len(offers[i])):
                    offers[i][j].print_everything_about_offer()
            for i in range(len(demands)):
                for j in range(len(demands[i])):
                    demands[i][j].print_everything_about_demand()

        #UPDATING STATES
        for j in range(self.NUM_STOCKS):
            self.state[self.NUM_AGENTS*self.NUM_STOCKS + self.NUM_AGENTS + j] = self.profit


        for i in range(len(demands)):
            max_price = 0
            volume = 0
            if (len(demands[i]) == 0):
                max_price = self.state[self.NUM_AGENTS*self.NUM_STOCKS + self.NUM_AGENTS + self.NUM_STOCKS + i]
            for j in range(len(demands[i])):
                if (max_price <= demands[i][j].price):
                    max_price = demands[i][j].price
                    volume = demands[i][j].amount
            #change state
            self.state[self.NUM_AGENTS*self.NUM_STOCKS + self.NUM_AGENTS + self.NUM_STOCKS + i] = max_price
            self.state[self.NUM_AGENTS*self.NUM_STOCKS + self.NUM_AGENTS + 2*self.NUM_STOCKS + i] = volume

        for i in range(len(offers)):
            min_price = 0
            volume = 0
            if (len(offers[i])==0):
                min_price = self.state[self.NUM_AGENTS*self.NUM_STOCKS + self.NUM_AGENTS + 3*self.NUM_STOCKS + i] 
            else:
                min_price = offers[i][0].price
                volume = offers[i][0].amount
            for j in range(len(offers[i])):
                if (min_price >= offers[i][j].price):
                    min_price = offers[i][j].price 
                    volume = offers[i][j].amount
            #change state
            self.state[self.NUM_AGENTS*self.NUM_STOCKS + self.NUM_AGENTS + 3*self.NUM_STOCKS + i] = min_price
            self.state[self.NUM_AGENTS*self.NUM_STOCKS + self.NUM_AGENTS + 4*self.NUM_STOCKS + i] = volume

        #ACTUAL TRADING TRANSACTION - ONE TIME
        self.transaction(offers, demands, print_info)
        #current version just for one stock
        #if not self.observation_space.contains(obs):
            #print('Observations are not proper ')

        for i in range(self.NUM_AGENTS):
            for j in range(self.NUM_STOCKS):
                r = 0 
                r = r + self.profit*self.state[i*self.NUM_STOCKS + j] 
                print ("REWARD IS")
                print(r)
            reward.append(r)

        return self.state, r, self.done, {}

    def reset(self):
        self.round = 0
        self.state = np.array(self.NUM_AGENTS*self.NUM_STOCKS*[0.25] + [40]*self.NUM_AGENTS + [self.array_values[self.round]]*self.NUM_STOCKS + 4*[0]*self.NUM_STOCKS)
        a = np.array(self.NUM_AGENTS*self.NUM_STOCKS*[0.25] + [40]*self.NUM_AGENTS + [self.array_values[self.round]]*self.NUM_STOCKS + 4*[0]*self.NUM_STOCKS)

        return (a)



