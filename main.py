from flask import Flask, render_template, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "HelloFaateh123"
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.String(250), nullable=False)
    has_wifi = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.String(250), nullable=False)
    can_take_calls = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return dictionary

class CafeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "e.g., Starbucks"})
    map_url = StringField("Map URL", validators=[DataRequired()], render_kw={"placeholder": "Google Maps URL"})
    img_url = StringField("Image URL", validators=[DataRequired()], render_kw={"placeholder": "Google Image URL"})
    location = StringField("City", validators=[DataRequired()], render_kw={"placeholder": "e.g., Los Angeles"})
    seats = StringField("Number of Seats", validators=[DataRequired()], render_kw={"placeholder": "e.g., 10-20 or 20+"})
    toilet = StringField("Bathrooms?", validators=[DataRequired()], render_kw={"placeholder": "True or False"})
    wifi = StringField("WiFi?", validators=[DataRequired()], render_kw={"placeholder": "True or False"})
    sockets = StringField("Power Outlets?", validators=[DataRequired()], render_kw={"placeholder": "True or False"})
    calls = StringField("Takes Calls?", validators=[DataRequired()], render_kw={"placeholder": "True or False"})
    price = StringField("Price", validators=[DataRequired()], render_kw={"placeholder": "e.g. $2.13 or €2.97"})
    submit = SubmitField("Submit", validators=[DataRequired()])


@app.route("/")
def home():
    cafes = db.session.query(Cafe).all()
    return render_template("index.html", all_cafes=cafes)


@app.route("/all")
def get_all():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafe=[i.to_dict() for i in cafes])

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    cafe = CafeForm()
    if cafe.validate_on_submit():
        new_cafe = Cafe(
            name=cafe.name.data,
            map_url=cafe.map_url.data,
            img_url=cafe.img_url.data,
            location=cafe.location.data,
            seats=cafe.seats.data,
            has_toilet=cafe.toilet.data.upper(),
            has_wifi=cafe.wifi.data.upper(),
            has_sockets=cafe.sockets.data.upper(),
            can_take_calls=cafe.calls.data.upper(),
            coffee_price=cafe.price.data,
        )
        if new_cafe:
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("add.html", form=cafe)

@app.route("/delete/<int:cafe_id>")
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))





if __name__ == "__main__":
    app.run(debug=True)



