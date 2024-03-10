from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///about.db"
db = SQLAlchemy(app)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(80), nullable=False)
    about = db.relationship("About", backref="country", uselist=False)


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(30), unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)


@app.route("/inf")
def index():
    country = Country(country_name="Ukraine")
    about = About(language="Ukranian",
                  phone_number="+380",
                  country=country)

    db.session.add(country)
    db.session.add(about)
    db.session.commit()

    return "Success"


@app.route("/country/<int:country_id>/about")
def info(country_id):
    country = Country.query.get_or_404(country_id)
    about = country.about
    if about:
        return f"{about.id}, {about.language}, {about.phone_number}"
    else:
        return "There no information about this country currently"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
