from flask import Flask, render_template, request, jsonify, send_from_directory, redirect
from json import loads
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask('__name__')
app.secret_key = 'celeb_by_qeens'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jtdrukkmcjtktf:02991bc640eade3baab406b31c5b6cd61bb0c6739a8bc37fb84d5afbdff238f3@ec2-54-84-98-18.compute-1.amazonaws.com:5432/dek9mol2100l7c'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

urls = {
    'home': '/',
    'wish': '/<string:lnk>',
    'favicon': '/favicon.ico',
    'users': '/users'
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
        return str({
            'id': self.id,
            'name': self.name,
            'b64_img': self.b64_img,
            'msg': self.msg
        })


# home page handler
@app.route(urls['home'], methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        data = loads(request.form['data'])
        name = data['name'].lower()
        user: User = User(name, data['image'], data['msg'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'ret_val': True, 'lnk': name.replace(' ', '-') + '-' + str(user.id) })
    return render_template('link.html', title='Qeens Wish')


@app.route(urls['users'])
def users_():
    users = [{'name': x.name.title(), 'url': x.name.replace(' ', '-') + '-' + str(x.id)} for x in User.query.all()]
    return render_template('users.html', title='Users', users=users, len=len(users))


@app.route(urls['favicon'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


def b(ns: list) -> str:
    ret = ''
    for h in ns[:-1]:
        ret += h+" "
    return ret[:-1]


@app.route(urls['wish'])
def wish(lnk: str):
    details = lnk.split('-')
    user: User = User.query.filter_by(name=b(details).lower(), id=int(details[-1])).first()
    if user is not None:
        return render_template('wish.html', user=user, title=user.name+' Wishes')
    return redirect('/', 200)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)
