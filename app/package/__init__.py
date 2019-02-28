from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

package = Flask(__name__)
package.config.from_object(Config)
db = SQLAlchemy(package)
migrate = Migrate(package, db)

from package import routes, models