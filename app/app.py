import os
import redis
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine

USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
DB = os.environ["DB"]

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]

ACTIVE_DB = os.environ["ACTIVE_DB"]

db = SQLAlchemy()
db_mongo = MongoEngine()
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def create_app():
    app = Flask(__name__)
    app.config.from_mapping({
        "SQLALCHEMY_DATABASE_URI": f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DB}",
    })
    
    app.config["MONGODB_SETTINGS"] = [{
        "db": "zno",
        "host": "mongo",
        "port": 27017
    }]
    
    @app.cli.command("migrate-mongo")
    def migrate_mongo():
        from scripts.postgres_to_mongo import migrate
        migrate()        
 
    db.init_app(app)
    with app.app_context():
        db.reflect()
        
    db_mongo.init_app(app)

    import views
    app.register_blueprint(views.student_bp)
    app.register_blueprint(views.test_bp)
    app.register_blueprint(views.query_bp)
    
    @app.route("/", methods=["GET", "POST"])
    def root():
        return redirect(url_for("student.student_all"))

    return app