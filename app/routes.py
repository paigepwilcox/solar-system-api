from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planets import *


planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"planet {model_id} invalid"}, 400))
    
    planet = cls.query.get(model_id)

    if not planet:
        abort(make_response({"message":f"planet {model_id} not found"}, 404))
    return planet

@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    new_planet = Planets(name=request_body["name"],
                        description=request_body["description"])
    
    db.session.add(new_planet)
    db.session.commit()

    return make_response(jsonify(f"Planet {new_planet.name} successfully created"), 201)


@planets_bp.route("", methods=["GET"])
def read_all_planets():
    # planets = Planets.query.all()
    title_query = request.args.get("title")
    if title_query:
        planets = Planets.query.filter_by(title=title_query)
    else:
        planets = Planets.query.all()

    planets_response = []
    for planet in planets:
        planets_response.append(planet.to_dict())
    return jsonify(planets_response)

@planets_bp.route("/<planet_id>", methods=["GET"])
def read_one_planet(planet_id):
    planet = validate_model(Planets, planet_id)
    return planet.to_dict()


@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_model(Planets, planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]

    db.session.commit()
    return make_response(f"Planet #{planet.id} successfully updated", 200)


@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_model(Planets, planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"Planet #{planet.id} successfully deleted!", 200)
