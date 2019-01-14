from lib.misc.misc import singleton
import json
import pkg_resources
import lib.evestatic.evestatic as evestatic

@singleton
class blueprints():
	def __init__(self):
		self.blueprint_json = json.load(open(pkg_resources.resource_filename(__name__,"blueprints.json")))
	def get_raw(self):
		return self.blueprint_json
	def getAllBlueprintIds(self):
		return list(self.blueprint_json)
	def isReaction(self,blueprint_id):
		return 'reaction' in self.blueprint_json[str(blueprint_id)]["activities"]
	def getBlueprintMaterials(self,blueprint_id):
		if str(blueprint_id) not in self.blueprint_json:
			return None
		if ("manufacturing" in self.blueprint_json[str(blueprint_id)]["activities"]):
			return self.blueprint_json[str(blueprint_id)]["activities"]["manufacturing"].get("materials",None)
		if ('reaction' in self.blueprint_json[str(blueprint_id)]["activities"]):
			return self.blueprint_json[str(blueprint_id)]["activities"]["reaction"].get("materials",None)
		return None
	def getBlueprintProducts(self,blueprint_id):
		if ("manufacturing" in self.blueprint_json[str(blueprint_id)]["activities"]):
			return self.blueprint_json[str(blueprint_id)]["activities"]["manufacturing"].get("products",None)
		if ('reaction' in self.blueprint_json[str(blueprint_id)]["activities"]):
			return self.blueprint_json[str(blueprint_id)]["activities"]['reaction'].get("products",None)
		return None
	def calc_compression(self,blueprint_id,filter_input = None):
		sd = evestatic.get_evestatic()
		sum_func = lambda items: sum(map(lambda item: sd.getItem(item["typeID"])["volume"] * item['quantity'],items))
		input = self.getBlueprintMaterials(blueprint_id)
		if(filter_input):
			input = filter(filter_input,input)
		output = self.getBlueprintProducts(blueprint_id)
		return float(sum_func(input))/sum_func(output) if(input != None and output!= None) else None
	def getBlueprint(self, product_id):
		for bpid in self.blueprint_json:
			products = self.getBlueprintProducts(bpid)
			if(products != None):
				for product in products:
					if(product["typeID"] == product_id):
						return bpid
		return None
	def calc_prod_time(self,blueprint_id,runs,TE):
		if str(blueprint_id) not in self.blueprint_json:
			return 0
		baseProductionTime = self.blueprint_json[str(blueprint_id)]["activities"]['manufacturing']["time"]
		#Calculating skills...
		skills = self.blueprint_json[str(blueprint_id)]["activities"]['manufacturing']["skills"]
		#print skills
		skillModifier = 1.0
		for skill in skills:
			skillModifier = skillModifier * (1- 0.01 * 5) #Assuming all V here... skillLevel.get(skill["typeID"],5)
		#print "SkillModifier:", skillModifier
		#Calculating TimeModifier...
		TE_modifier = float(100-TE)/100
		facility_modifier = 1#0.58 # Keepstar in 1-dq
		Industry_skill_modifier = 0.8
		AdvIndustry_skill_modifier = 0.85
		timeModifier = TE_modifier* facility_modifier*Industry_skill_modifier*AdvIndustry_skill_modifier
		#print "timeModifier:", timeModifier
		#Calculating Actual production time...
		productionTime = baseProductionTime * timeModifier * skillModifier * runs
		return productionTime