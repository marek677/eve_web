from flask import Blueprint
from flask import render_template
import json
import datetime
from lib.market.market import *
from lib.industry.blueprints import *
from lib.evestatic.evestatic import *
test = Blueprint("test",__name__,template_folder='templates', static_url_path="web/components/test/static")

@test.route('/test_industry_time')
def test_industry_time():
	sd = get_evestatic()
	runs = 8
	raw_time = blueprints().calc_prod_time(22547,runs,20)
	time_human = "%d days %d hours %d minutes" %(raw_time/(24*60*60),raw_time%(24*60*60)/(60*60),raw_time%360/60)
	out = [
		{"item": sd.getItem(22547)["name"], "quantity" : runs, "time" : time_human},
	]
	for material in blueprints().getBlueprintMaterials(22547):
		blueprint_id = blueprints().getBlueprint(material["typeID"])
		time_human = "-"
		if(blueprint_id != None):
			raw_time = blueprints().calc_prod_time(blueprint_id,runs*material["quantity"],20)
			time_human = "%d days %d hours %d minutes" %(raw_time/(24*60*60),raw_time%(24*60*60)/(60*60),raw_time%360/60)
		#change this item to blueprint_id ?
		out.append({"item": sd.getItem(material["typeID"])["name"],"quantity": material["quantity"]*runs,"time" : time_human} )
	
	return render_template('test.html',output = out)

def getMarketStats(itemid):
	JitaSell = Market().getSellOrders(itemid)
	out = {"item": get_evestatic().getItem(itemid)["name"] ,"min" : min(JitaSell,key=lambda x: x["price"]).get("price",-1), "max": max(JitaSell,key=lambda x: x["price"]).get("price",-1), "ordercount": len(JitaSell),
		"median": sorted(JitaSell,key=lambda x: x["price"])[len(JitaSell)//2].get("price",-1), "avarage" : sum(map(lambda x: x["price"],JitaSell))/len(JitaSell) }
	return out		
	
@test.route('/test_market')
def test_market():
	items_in = [34,35,36]
	return render_template('market_view.html',market_table = map(getMarketStats,items_in))

def getReactionTableInner(result_id,multiplier):
	sd = get_evestatic()
	bp = blueprints()
	M = Market()
	bpid =  bp.getBlueprint(result_id)
	o_materials = []
	for material in bp.getBlueprintMaterials(bpid):
		o_materials.append({"item": sd.getItem(material["typeID"])["name"], "quantity": material["quantity"] * multiplier, "ISK" : multiplier*M.getJitaSell(material["typeID"]) * material["quantity"] }) 
	bpid_prod = bp.getBlueprintProducts(bpid)[0]
	o = {"result": {"item": sd.getItem(bpid_prod["typeID"])["name"], "quantity": multiplier*bpid_prod["quantity"], "ISK" : multiplier*M.getJitaSell(bpid_prod["typeID"]) * bpid_prod["quantity"]}, "materials" : o_materials }
	earn = o["result"]["ISK"] - sum(map(lambda x: x["ISK"],o["materials"]))
	o.update({"earn" : earn})
	return o

def getReactionTable(result_id):
	out = []
	bp = blueprints()
	out.append(getReactionTableInner(result_id,2))
	for material in bp.getBlueprintMaterials(bp.getBlueprint(result_id)):
		bpid = bp.getBlueprint(material["typeID"])
		if(bpid != None and bp.isReaction(bpid) == True):	
			out.append(getReactionTableInner(material["typeID"],1))
	return {"inter" : out, "total_earn" : sum(map(lambda x: x["earn"],out))}
@test.route('/test_reaction')	
def test_reactions():
	a = [16670,16671,16672,16673]
	return render_template('reactions.html',out = map(getReactionTable,a))