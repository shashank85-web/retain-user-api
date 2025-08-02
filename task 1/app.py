from flask import Flask
from routes.user_routes import user_bp
from database import db
import config

app = Flask(__name__)
app.config.from_object(config.Config)

db.init_app(app)
app.register_blueprint(user_bp)

@app.route("/")
def health_check():
    return {"status": "OK"}, 200

if __name__ == "__main__":
    app.run(debug=True)
