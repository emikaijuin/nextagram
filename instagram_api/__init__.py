from app import app, csrf
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Configure CORS settings
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Create JWT tokens to track API users
app.config['JWT_SECRET_KEY'] = "thisisasecret"
jwt = JWTManager(app)

## API Routes ##
from instagram_api.blueprints.users.views import users_api_blueprint
from instagram_api.blueprints.sessions.views import sessions_api_blueprint

csrf.exempt(users_api_blueprint)
csrf.exempt(sessions_api_blueprint)

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/sessions')
