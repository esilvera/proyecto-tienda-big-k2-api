from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    user_lname = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(100), nullable=False )
    user_role = db.Column(db.Boolean(), default=False)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_lname": self.user_lname,
            "user_email": self.user_email,
            "user_role": self.user_role
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Products(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer(), primary_key=True)
    product_name = db.Column(db.String(50), nullable=False)
    product_desc = db.Column(db.String(150))
    product_brand = db.Column(db.String(100))
    product_price = db.Column(db.Integer(), nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey("products_type.type_id", ondelete='CASCADE'), nullable=False)
    #product_type = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_desc": self.product_desc,
            "product_brand": self.product_brand,
            "product_price": self.product_price,
            "product_type_name": self.products_type.type_name #traemos de la tabla products type el tipo de producto (repuesto / accesorio)
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Products_Type(db.Model):
    __tablename__ = 'products_type'
    type_id = db.Column(db.Integer(), primary_key=True)
    type_name = db.Column(db.String(50), nullable=False)
    products = db.relationship("Products", cascade="all, delete", backref="products_type")

    def serialize(self):
        return {
            "type_id": self.type_id,
            "type_name": self.type_name
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Services(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer(), primary_key=True)
    service_name = db.Column(db.String(50), nullable=False)
    service_desc = db.Column(db.String(150))
    service_icon = db.Column(db.String(50))

    def serialize(self):
        return {
            "service_id": self.service_id,
            "service_name": self.service_name,
            "service_desc": self.service_desc,
            "service_icon": self.service_icon
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Shopping_Card(db.Model):
    __tablename__ = 'shopping_card'
    shop_id = db.Column(db.Integer(), primary_key=True)
    shop_user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'), nullable=False)
    shop_product_id = db.Column(db.Integer(), db.ForeignKey('products.product_id'), nullable=False)
    shop_service_id = db.Column(db.Integer(), db.ForeignKey('services.service_id'), nullable=False)

    def serialize(self):
        return {
            "shop_id": self.shop_id,
            "shop_user_id": self.shop_user_id,
            "shop_product_id": self.shop_product_id,
            "shop_service_id": self.shop_service_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


