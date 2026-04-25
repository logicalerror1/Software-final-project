from app import app, db
from models import Product

with app.app_context():
    db.create_all()

    # Seed the menu if empty
    if not Product.query.first():
        products = [
            Product(name='Espresso', description='Strong and bold', price=30.0),
            Product(name='Latte', description='Smooth with steamed milk', price=40.0),
            Product(name='Cappuccino', description='Rich foam and espresso', price=35.0),
            Product(name='Americano', description='Espresso with hot water', price=30.0),
            Product(name='Mocha', description='Chocolate and coffee', price=45.0)
        ]
        db.session.add_all(products)
        db.session.commit()
        print("Menu seeded successfully.")
    else:
        print("Menu already exists.")
