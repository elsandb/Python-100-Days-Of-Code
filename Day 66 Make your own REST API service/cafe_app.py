import os
from dotenv import load_dotenv, dotenv_values, find_dotenv
from sqlalchemy import exc
from flask import Flask, jsonify, render_template, request  # https://www.adamsmith.haus/python/docs/flask.jsonify
from flask_sqlalchemy import SQLAlchemy
import random

load_dotenv(find_dotenv('.env'))

app = Flask(__name__)
# # --- Configure App, make database
db_path = os.getenv("DB_PATH")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
# Todo: Encoding... Serialize objects to ASCII-encoded JSON, so that the
#   pound-symbol is shown correctly. This has security implications when rendering JSON into JavaScript in templates.
#   See https://flask.palletsprojects.com/en/2.2.x/config/#JSON_AS_ASCII.
#   https://en.wikipedia.org/wiki/URL_encoding
db = SQLAlchemy(app)


# Café table configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """Return dict on the form {column_name: column:value, ...}"""
        dictionary = {}
        for column in self.__table__.columns:  # Loop through each column in the data record.
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


@app.route("/")
def home():
    return render_template("index.html")


# --- HTTP GET - Read Record(s)
@app.route('/cafes')
def get_all():
    all_cafes = db.session.query(Cafe).all()  # --> [<Cafe 1>, <Cafe 2>, ..., <Cafe 21>]
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route('/cafes/random_cafe')  # GET is allowed by default on all routes.
def get_random():
    # cafe_count = Cafe.query.count()   # Get number of cafés in the database.
    random_cafe_id = random.randint(1, cafe_count := Cafe.query.count())  # Just to test the walrus operator ^^
    random_cafe = db.session.get(Cafe, random_cafe_id)
    print(random_cafe.coffee_price)
    return jsonify(random_cafe.to_dict())


@app.route('/cafes/by_location', methods=["GET"])
def search_location():
    args = request.args
    loc_entry = args.get("location").title()  # Get arg for 'location' and make it pascal case.
    cafes_at_location = db.session.query(Cafe).filter_by(location=loc_entry).all()
    if cafes_at_location:
        return jsonify(cafes_at_loc_entry=[cafe.to_dict() for cafe in cafes_at_location])
    else:
        return jsonify(error={"Not found": f"No cafes for the location '{loc_entry}' were found."})\
            , 404   # Resource not found


@app.route("/new_cafe", methods=["POST"])
def post_new_cafe():
    # The form data is sent as key-value pairs in the body of an HTTP POST request.
    try:
        new_cafe = Cafe(
            name=str(request.form.get("name").title()),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(int(request.form.get("has_sockets"))),
            has_toilet=bool(int(request.form.get("has_toilet"))),
            has_wifi=bool(int(request.form.get("has_wifi"))),
            can_take_calls=bool(int(request.form.get("can_take_calls"))),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
    except exc.IntegrityError:
        return jsonify({"Error": "The café name already exist in the database."}), 409  # Conflict
    else:
        return jsonify(response={"success": "Successfully added the new cafe."}), 200


# # HTTP PUT/PATCH - Update Record
@app.route("/cafe/<int:cafe_id>/price", methods=["PATCH"])
def update_price_by_id(cafe_id: int):
    cafe = db.session.get(entity=Cafe, ident=cafe_id)
    new_price = request.args.get('new_price')  # Argument passed in the PATCH request.

    if not cafe:    # If café == NonType object.
        return jsonify({"error":
                            {"Not Found": f"No cafe with id '{cafe_id}' were found in the database."}
                        }), 404 # Not found

    elif not new_price:  # If new_price == None
        return jsonify({"error":
                            {"Invalid parameter name": f"The only valid parameter name is 'new_price'"}
                        }), 404  # Not found
    else:
        cafe = db.session.get(entity=Cafe, ident=cafe_id)
        cafe.coffee_price = new_price  # Update café in the database:
        db.session.commit()
        return jsonify({"success": "Successfully updated the price."})


# # HTTP DELETE - Delete Record
@app.route("/cafe/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id: int):
    cafe_to_delete = db.session.get(entity=Cafe, ident=cafe_id)
    api_key = request.args.get("api-key")
    if api_key != "TopSecretAPIKey":
        return {"error": "Sorry, you are not authorized to delete a café from the database. "
                         "Make sure you have the correct api-key."}, 403  # Forbidden
    if cafe_to_delete is None:
        return jsonify({"error":
                            {"Not Found": f"No cafe with the id '{cafe_id}' were found in the database."}
                        }), 404  # Not found
    if cafe_to_delete is not None:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify({"success": f"The café with ID {cafe_id} was successfully deleted."})


if __name__ == '__main__':
    app.run(debug=True)
