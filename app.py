import os
import webbrowser

import werkzeug
from flask import Flask, render_template, request, json, session, send_file, g
from models.models import db, Users, Reviews
from flask import make_response
from flask_talisman import Talisman, ALLOW_FROM
from pathlib import Path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
# talisman = Talisman(app)

csp = {
    'default-src': [
        '\'self\'',
        'https://ajax.googleapis.com',
        'http://netdna.bootstrapcdn.com'
    ]
}

@app.errorhandler(500)
def handle_internal_server_error(error):
    return str(error)


@app.route("/")
def main():
    if not session.get('logged_in'):
        return render_template('login.html')

    return render_template('login.html')


@app.route('/home', methods=['POST'])
# @talisman(content_security_policy=csp)
def login():
    _username = request.form['username']
    _password = request.form['inputPassword']

    if _username and _password:
        all_data = None
        try:
            data = Users.query.filter_by(user_username=_username, user_password=_password).first()
        except Exception as ex:
            raise Exception(ex)

        # Populate all hotel reviews
        all_data = Reviews.query.order_by(Reviews.review_id.desc()).limit(9).all()

        if data is not None:
            session['logged_in'] = True
            return render_template('index.html', items=all_data, section="hero")
        else:
            return "No user found"

    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


@app.route('/home/submitted_review', methods=['POST'])
# @talisman(content_security_policy=csp)
def writeblog():
    _review_hotel = request.form['hotel']
    _review_city = request.form['city']
    _review_body = request.form['review']
    _review_rating = request.form['rating']

    try:
        review = Reviews(review_hotel=_review_hotel, review_city=_review_city, review_body=_review_body, review_rating=_review_rating)
        db.session.add(review)
        db.session.commit()
    except Exception as e:
        print (e)
        db.session.rollback()

    r = make_response(render_template('index.html', section="features"))
    r.headers.set('Content-Security-Policy', "default-src 'self'")
    return r


@app.route('/home', methods=['GET'])
# @talisman(content_security_policy=csp)
def search():
    if not session.get('logged_in'):
        return render_template('login.html')
    try:
        _search_term = request.args['search_input']
    except werkzeug.exceptions.BadRequest:
        all_data = Reviews.query.order_by(Reviews.review_id.desc()).limit(9).all()
        return render_template('index.html', items=all_data)

    try:
        data = Reviews.query.filter(Reviews.review_hotel.like("%{0}%".format(_search_term)) |
                                    Reviews.review_city.like("%{0}%".format(_search_term)) |
                                    Reviews.review_body.like("%{0}%".format(_search_term)) |
                                    Reviews.review_rating.like("%{0}%".format(_search_term))).all()

    except Exception as e:
        print (e)
        db.session.rollback()

    g.search_term = _search_term
    r = make_response(render_template('index.html', items=data, section="features"))
    r.headers.set('Content-Security-Policy', "default-src 'self'")
    return r


@app.route("/logout")
# @talisman(content_security_policy=csp)
def logout():
    session['logged_in'] = False
    app.secret_key = os.urandom(12)
    return render_template('login.html')


@app.route('/home/getfiles', methods=['GET'])
# @talisman(content_security_policy=csp)
def get_file():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        file = request.args['file']
        my_file = Path("static/" + file)
        if my_file.is_file():
            return send_file(file)
        else:
            return "Operation not allowed"


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', debug=True)