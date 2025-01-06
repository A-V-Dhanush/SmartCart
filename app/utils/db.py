from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from app.models import User, Cart, Product  # Import models
    db.create_all()  # Create tables
