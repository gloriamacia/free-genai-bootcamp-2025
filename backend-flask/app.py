from lib.db import Db

import routes.words
import routes.groups
import routes.study_sessions
import routes.dashboard
import routes.study_activities

from flask import Flask, jsonify
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_mapping(
            DATABASE='words.db'
        )
    else:
        app.config.update(test_config)

    # Initialize database
    app.db = Db(database=app.config['DATABASE'])

    # Allow CORS for all origins & methods
    CORS(app, resources={r"/*": {"origins": ["*"], "allow_headers": "*", "methods": "*"}})

    # Close database connection
    @app.teardown_appcontext
    def close_db(exception):
        app.db.close()

    # Load routes
    routes.words.load(app)
    routes.groups.load(app)
    routes.study_sessions.load(app)
    routes.dashboard.load(app)
    routes.study_activities.load(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
