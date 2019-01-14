from flask import Blueprint
from flask import render_template
from lib.industry.blueprints import *
import lib.evestatic.evestatic as evestatic
from lib.market.market import *
import time
industry = Blueprint("industry",__name__,template_folder='templates')

@industry.route('/indy_compression')
def indy_compression():
	start = time.time()
	sd = evestatic.get_evestatic()
	a = blueprints().getAllBlueprintIds()
	m = Market()
	ff = filter(lambda b_id: m.isItemInMarket(int(b_id)) == True, a)
	table = map(lambda b_id: [sd.getItem(b_id)["name"],blueprints().calc_compression(b_id)], ff)
	lit_table = sorted(filter(lambda x: x[1] > 1,table),key=lambda x:x[1],reverse=True)
	print "Indy_comp:", time.time() - start
	return render_template('indy_test.html', my_table = lit_table)