
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, current_app  
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakeries_list)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    with current_app.app_context():  
        bakery = db.session.get(Bakery, id)  
        if bakery is None:
            return make_response(jsonify({'error': 'Bakery not found'}), 404)
        bakery_dict = bakery.to_dict()
        bakery_dict['baked_goods'] = [baked_good.to_dict() for baked_good in bakery.baked_goods]
        return jsonify(bakery_dict)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return jsonify(most_expensive.to_dict())

if __name__ == '__main__':
    app.run(port=5555, debug=True)
