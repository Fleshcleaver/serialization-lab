from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import fields

db = SQLAlchemy()
ma = Marshmallow()


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer')

    # Association proxy to get items through reviews
    items = association_proxy('reviews', 'item')


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates='item')


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')


# ── Schemas ──────────────────────────────────────────────────────────────────

class ReviewSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Review
        load_instance = True

    id = ma.auto_field()
    comment = ma.auto_field()
    customer_id = ma.auto_field()
    item_id = ma.auto_field()

    # Nested but exclude back-references to avoid recursion
    customer = fields.Nested(lambda: CustomerSchema(exclude=('reviews',)))
    item = fields.Nested(lambda: ItemSchema(exclude=('reviews',)))


class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()

    reviews = fields.List(fields.Nested(lambda: ReviewSchema(exclude=('customer',))))


class ItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Item
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    price = ma.auto_field()

    reviews = fields.List(fields.Nested(lambda: ReviewSchema(exclude=('item',))))