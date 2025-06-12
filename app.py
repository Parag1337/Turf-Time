from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from flask_mail import Mail
from datetime import datetime
from config import Config
from database.models import db, User

# Initialize Flask extensions
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Add the FakeUser class for template testing
class FakeUser:
    is_authenticated = True
    is_active = True
    role = 'user'
    username = 'TestUser'
    def get_id(self):
        return '1'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)    # Initialize Flask-Mail
    mail.init_app(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.owner import owner_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(owner_bp)
    
    # Custom Jinja2 filters
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        if not text:
            return ""
        return text.replace('\n', '<br>')
    
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.is_owner():
                return redirect(url_for('owner.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))
        return render_template('index.html')
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
      # Debug routes removed - no longer needed
    
    # Inject current_time into templates (but use Flask-Login's current_user)
    @app.context_processor
    def inject_context():
        return {'now': datetime.now()}
      # Configure logging for production
    if not app.debug:
        import logging
        logging.basicConfig(level=logging.WARNING)
    
    return app

if __name__ == '__main__':
    app = create_app()
      # Create database tables (remove in production)
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
