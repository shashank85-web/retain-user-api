from flask import Blueprint, request, jsonify
from models.user import User
from schemas.user_schema import UserSchema
from database import db
from utils.password import hash_password, check_password

user_bp = Blueprint("user_bp", __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return users_schema.dump(users), 200

@user_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    return (user_schema.dump(user), 200) if user else ({"error": "User not found"}, 404)

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"error": "Email already exists"}, 409

    new_user = User(
        name=data["name"],
        email=data["email"],
        password_hash=hash_password(data["password"])
    )
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user), 201

@user_bp.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    data = request.get_json()
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        if User.query.filter_by(email=data["email"]).first():
            return {"error": "Email already exists"}, 409
        user.email = data["email"]
    db.session.commit()
    return user_schema.dump(user), 200

@user_bp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted"}, 200

@user_bp.route("/search")
def search_user():
    name = request.args.get("name")
    if not name:
        return {"error": "Missing 'name' parameter"}, 400

    users = User.query.filter(User.name.contains(name)).all()
    return users_schema.dump(users), 200

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password required"}, 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password(password, user.password_hash):
        return {"error": "Invalid credentials"}, 401

    return {"message": "Login successful", "user": user_schema.dump(user)}, 200
