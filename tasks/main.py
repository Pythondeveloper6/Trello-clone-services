from app.api.boards import board_bp
from app.api.projects import projects_bp
from app.api.tasks import tasks_bp
from app.core.config import settings
from app.db.database import Base, create_tables
from flask import Flask, jsonify
from flask_migrate import Migrate

# global migration object
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    # intiate flask-migrate
    migrate.init_app(app, db=None, directory="migrations")

    # register app routes : blueprints
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(board_bp)
    return app


app = create_app()


def start_tasks():
    create_tables()


with app.app_context():
    start_tasks()


# health checker endpoint
@app.route("/health")
def health_check():
    return jsonify(
        {
            "service": settings.SERVICE_NAME,
            "status": "healthy",
            "version": settings.VERSION,
        }
    )


if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
