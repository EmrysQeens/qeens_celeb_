from flask import Flask, render_template, request, jsonify, send_from_directory
from json import loads
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask('__name__')
app.secret_key = 'celeb_by_qeens'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

urls = {
    'home': '/',
    'wish': '/<string:lnk>',
    'favicon': '/favicon.ico'
}

db: SQLAlchemy = SQLAlchemy(app)


class User(db.Model):   # User model to save name and image
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    b64_img = db.Column(db.Text, nullable=True, unique=False)
    msg = db.Column(db.Text, nullable=False, unique=False)

    def __init__(self, name, b64_img, msg):
        self.name = name
        self.b64_img = b64_img
        self.msg = msg

    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'b64_img': self.b64_img,
            'msg': self.msg
        }


# home page handler
@app.route(urls['home'], methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        data = loads(request.form['data'])
        user: User = User(data['name'].lower(), data['image'], data['msg'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'ret_val': True, 'lnk': str(user.id) + user.name})
    return render_template('link.html', home=True)


@app.route(urls['favicon'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route(urls['wish'])
def wish(lnk: str):
    [id_, name] = lnk.split('-')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)