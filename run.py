import pkg_resources
import sys
import os
import main.main


if __name__ == "__main__":
	sys.path.append(pkg_resources.resource_filename(__name__,"lib"))
	app = main.main.app
	app.config.update(dict(
		BASE_DIR=os.getcwd(),
	))
	main.main.preload()
	app.run()