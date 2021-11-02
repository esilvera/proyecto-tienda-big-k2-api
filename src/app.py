from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users, Products, Products_Type, Services, Shopping_Card
import datetime


app = Flask(__name__)
app.url_map.slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['JWT_SECRET_KEY'] = 'eb17823728014753b605e18e32c932b5'

db.init_app(app)
Migrate(app, db)  # db init,  db migrate,  db upgrade
jwt = JWTManager(app)
CORS(app)


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/api/register", methods=['POST'])
def register():
    user_name = request.json.get('user_name')
    user_lname = request.json.get('user_lname')
    user_email = request.json.get('user_email')
    user_password = request.json.get('user_password')
    user_role = request.json.get('user_role', 0)

    user = Users.query.filter_by(user_email=user_email).first()
    if user: return jsonify({"msg": "Email ya esta en uso."}), 400

    user = Users()
    user.user_name = user_name
    user.user_lname = user_lname
    user.user_email = user_email
    user.user_password = generate_password_hash(user_password)
    user.user_role = user_role
    user.save()

    return jsonify({"msg": "Usuario registrado, por favor inicie sesion"}), 201

@app.route("/api/login", methods=['POST'])
def login():
    user_email = request.json.get("user_email")
    user_password = request.json.get("user_password")

    user = Users.query.filter_by(user_email=user_email).first() # Podemos agregar un filtro para los level = 1 (, level=True)
    if not user: 
        return jsonify({"msg": "Usuario/Password no se encuentran."}), 400

    if not check_password_hash(user.user_password, user_password): 
        return jsonify({"msg": "Usuario/Password no se encuentran."}), 400

    expire = datetime.timedelta(minutes=5)
    print(expire)

    access_token = create_access_token(identity=user.user_email, expires_delta=expire)

    data = {
        "access_token": access_token,
        "user": user.serialize()
    }

    return jsonify(data), 200

@app.route("/api/users", methods=['GET'])
@jwt_required()
def users():
    users = Users.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@app.route("/api/profile", methods=['GET'])
@jwt_required()
def profile():
    identity = get_jwt_identity()
    user = Users.query.filter_by(user_email=identity).first()
    return jsonify({"identity": identity, "user": user.serialize()}),200

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):

    user = Users.query.get(id)

    if not user: return jsonify({"status": False, "msg": "User doesn't exist"}), 404

    user.delete()

    return jsonify({"status": True, "msg": "User deleted"}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Products.query.all()
    products = list(map(lambda products: products.serialize(), products))
    return jsonify(products), 200

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product_id(id):
    
    product = Products.query.get(id)
    if not product: return jsonify({"status": False, "msg": "Product doesn't exist"}), 404
    return jsonify(products.serialize()), 200

@app.route('/api/products', methods=['POST'])
def post_products():

    product_name = request.json.get('product_name')
    product_desc = request.json.get('product_desc')
    product_brand = request.json.get('product_brand')
    product_price = request.json.get('product_price')
    product_type_id = request.json.get('product_type_id')

    verify_name = Products.query.filter_by(product_name=product_name).first()
    #print(verify_name)
    if verify_name: 
        verify_brand = Products.query.filter_by(product_brand=product_brand).first()
        #print(verify_brand)
        if verify_brand:
            return jsonify({"status": True, "msg": "Product already exists"}), 404
    
    
    product = Products()
    product.product_name = product_name
    product.product_desc = product_desc
    product.product_brand = product_brand
    product.product_price = product_price
    product.product_type_id = product_type_id
    product.save()

    return jsonify(product.serialize()), 201

@app.route('/api/products/<int:id>', methods=['PUT'])
def put_product(id):

    #solo se deberia poder cambiar el precio
    product_price = request.json.get('product_price')

    products = Products.query.get(id)
    products.product_price = product_price
    products.update()

    return jsonify(products.serialize()), 200    

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):

    product = Products.query.get(id)

    if not product: return jsonify({"status": False, "msg": "Product doesn't exist"}), 404

    product.delete()

    return jsonify({"status": True, "msg": "Product deleted"}), 200

@app.route('/api/products_type', methods=['GET'])
def get_products_type():
    products_type = Products_Type.query.all()
    products_type = list(map(lambda products_type: products_type.serialize(), products_type))
    return jsonify(products_type), 200

@app.route('/api/products_type/<int:id>', methods=['GET'])
def get_products_type_id(id):
    
    product_type = Products_Type.query.get(id)
    if not product_type: return jsonify({"status": False, "msg": "Product type doesn't exist"}), 404
    return jsonify(product_type.serialize()), 200

@app.route('/api/products_type', methods=['POST'])
def post_products_type():

    type_name = request.json.get('type_name')

    products_type = Products_Type()
    products_type.type_name = type_name
    products_type.save()

    return jsonify(products_type.serialize()), 201

@app.route('/api/products_type/<int:id>', methods=['PUT'])
def put_product_type(id):

    type_name = request.json.get('type_name')

    products_type = Products_Type.query.get(id)
    products_type.type_name = type_name
    products_type.update()

    return jsonify(products_type.serialize()), 200 

@app.route('/api/products_type/<int:id>', methods=['DELETE'])
def delete_product_type(id):

    product_type = Products_Type.query.get(id)

    if not product_type: return jsonify({"status": False, "msg": "Product Type doesn't exist"}), 404

    product_type.delete()

    return jsonify({"status": True, "msg": "Product Type deleted"}), 200

@app.route('/api/services', methods=['GET'])
def get_services():
    services = Services.query.all()
    services = list(map(lambda services: services.serialize(), services))
    return jsonify(services), 200

@app.route('/api/services/<int:id>', methods=['GET'])
def get_services_id(id):
    
    service = Services.query.get(id)
    if not service: return jsonify({"status": False, "msg": "Service doesn't exist"}), 404
    return jsonify(service.serialize()), 200

@app.route('/api/services', methods=['POST'])
def post_services():

    service_name = request.json.get('service_name')
    service_desc = request.json.get('service_desc')

    verify_service = Services.query.filter_by(service_name=service_name).first()
    if verify_service: return jsonify({"status": True, "msg": "Service already exists"}), 404

    service = Services()
    service.service_name = service_name
    service.service_desc = service_desc
    service.save()

    return jsonify(service.serialize()), 201

@app.route('/api/services/<int:id>', methods=['PUT'])
def put_services(id):

    service_name = request.json.get('service_name')
    service_desc = request.json.get('service_desc')

    service = Services.query.get(id)
    service.service_name = service_name
    service.service_desc = service_desc
    service.update()

    return jsonify(service.serialize()), 200

@app.route('/api/services/<int:id>', methods=['DELETE'])
def delete_services(id):

    service = Services.query.get(id)

    if not service: return jsonify({"status": False, "msg": "Services doesn't exist"}), 404

    service.delete()

    return jsonify({"status": True, "msg": "Service deleted"}), 200

@app.route('/api/shopping_card', methods=['GET'])
def get_shopping_card():
    shopping_card = Shopping_Card.query.all()
    shopping_card = list(map(lambda shopping_card: shopping_card.serialize(), shopping_card))
    return jsonify(shopping_card), 200

@app.route('/api/shopping_card', methods=['POST'])
def post_shopping_card():

    shop_user_id = request.json.get('shop_user_id')
    shop_product_id = request.json.get('shop_product_id')
    shop_service_id = request.json.get('shop_service_id')

    shopping_card = Shopping_Card()
    shopping_card.shop_user_id = shop_user_id
    shopping_card.shop_product_id = shop_product_id
    shopping_card.shop_service_id = shop_service_id
    shopping_card.save()

    return jsonify(shopping_card.serialize()), 201

@app.route('/api/shopping_card/<int:id>', methods=['DELETE'])
def delete_shopping_card(id):

    shopping_card = Shopping_Card.query.get(id)

    if not shopping_card: return jsonify({"status": False, "msg": "Shopping Card ID doesn't exist"}), 404

    shopping_card.delete()

    return jsonify({"status": True, "msg": "Shopping Card ID deleted"}), 200





if __name__ == '__main__':
    app.run()