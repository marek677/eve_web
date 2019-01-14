from flask import current_app as app
import json
from lib.misc.misc import singleton
import time
@singleton 
class Market():
	def __init__(self,c_app = app):
		print "Initializing MarketViever"
		d = json.load(open(c_app.config["BASE_DIR"] + "/dumps/market_dump.json"))
		self.data = {}
		for dd in d:
			item_id = dd["item"]
			if(item_id not in self.data):
				self.data[item_id] = []
			self.data[item_id].append(dd)
		print "Finished init..."
	def isItemInMarket(self,itemid):
		#start = time.time()
		ret= itemid in self.data
		#print "isItemInMarket:",time.time() - start
		return ret
	def getAllOrders(self,itemid):
		return self.data[itemid]
	def getBuyOrders(self,itemid):
		return filter(lambda order: order["isBuy"] == True, self.data[itemid])
	def getSellOrders(self,itemid):
		return filter(lambda order: order["isBuy"] == False, self.data[itemid])
	def getJitaBuy(self,itemid):
		return max(filter(lambda order: order["isBuy"] == True and order["system"] == 30000142, self.data[itemid]), key=lambda x: x["price"]).get("price",-1)
	def getJitaSell(self,itemid):
		return min(filter(lambda order: order["isBuy"] == False and order["system"] == 30000142, self.data[itemid]), key=lambda x: x["price"]).get("price",-1)