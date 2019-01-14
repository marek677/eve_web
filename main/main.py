from flask import Flask
import pkg_resources
from lib.market.market import *

from blueprints.main.routes import main
from blueprints.industry.routes import industry
from blueprints.region.routes import region
from blueprints.test.routes import test

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(industry)
app.register_blueprint(region)
app.register_blueprint(test)


def preload():
	from lib.market.market import Market
	Market(app)