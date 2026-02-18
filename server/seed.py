from app import app
from models import db, Customer, Item, Review

with app.app_context():
    db.drop_all()
    db.create_all()

    # Customers
    c1 = Customer(name='Alice')
    c2 = Customer(name='Bob')

    # Items
    i1 = Item(name='Insulated Mug', price=9.99)
    i2 = Item(name='Wireless Headphones', price=49.99)

    db.session.add_all([c1, c2, i1, i2])
    db.session.commit()

    # Reviews
    r1 = Review(comment='Love this mug!', customer=c1, item=i1)
    r2 = Review(comment='Great headphones.', customer=c2, item=i2)
    r3 = Review(comment='Would buy again.', customer=c1, item=i2)

    db.session.add_all([r1, r2, r3])
    db.session.commit()

    print("Seeded database successfully!")