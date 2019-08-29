import gym_tradingmulti.envs.tradingmulti_env as envir

class MarketAgent:

	def take_action(self):
		return 

class HardCodedAgentProducer(MarketAgent):
	def __init__(self):
		self.producer=True
		pass

	def set_producer(self, val):
		self.producer = val

	def take_action(self, stock):
		if self.producer:
			return envir.Demand(0.2, 0.2, 1, stock)
		else:
			return envir.Offer(0.5, 0.15, 2, stock)

	# def add_to_action(self, actions, stock):
	# 	actions.append(self.take_action(stock))



class LearningAgent(MarketAgent):

	def take_action(self, action, agent_index, stock_index, demand_stock, offer_stock):
		if (abs(action[3*agent_index*self.num_stocks+3*stock_index] - 1.00) < 0.01) and (action[3*agent_index*self.num_stocks+3*stock_index+2]>0) and (action[3*agent_index*self.num_stocks+3*stock_index+1] > 0):
			demand_stock.append(envir.Demand(action[3*agent_index*self.num_stocks+3*stock_index+2], action[3*agent_index*self.num_stocks+3*stock_index+1], agent_index, stock_index))
		elif (abs(action[3*agent_index*self.num_stocks+3*stock_index] - 2.00) < 0.01) and (action[3*agent_index*self.num_stocks+3*stock_index+2]>0) and (action[3*agent_index*self.num_stocks+3*stock_index+1]>0):
			offer_stock.append(envir.Offer(action[3*agent_index*self.num_stocks+3*stock_index+2], action[3*agent_index*self.num_stocks+3*stock_index+1], agent_index, stock_index))

	def add_to_action(self, action, agent_index, stock_index, demand_stock, offer_stock, actions):
		actions.append(self.take_action(action agent_index, stock_index, demand_stock, offer_stock))
			








			