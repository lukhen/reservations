from flask import Flask, g
from flask_cors import CORS
from project.model import count_all_reservations_sql, Db
import os


class ProductionConfig:
    DB_URI = os.environ.get("DB_URI")


def create_app(config=ProductionConfig):

    app = Flask(__name__)
    app.config.from_object(config)
    cors = CORS()
    cors.init_app(app)

    db_replica = Db(app.config["DB_URI"])

    @app.route("/allrescount")
    def allrescount():
        res_count = count_all_reservations_sql(db_replica.engine.connect())
        return render_the_number_of_reservations(res_count)

    return app


def render_the_number_of_reservations(num):
    return {"all_reservations": "{}".format(num)}
