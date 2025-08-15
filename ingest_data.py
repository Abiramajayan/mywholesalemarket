import random
import sys
import os

# This is a bit of a hack to make sure we can import from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from mywholesalemarket.app import app, db, Product

# Data from the HTML file's JavaScript, re-implemented in Python
CATEGORIES = [
    'DECK EQUIPMENT', 'ENGINE ROOM', 'ELECTRICAL', 'SAFETY EQUIPMENT',
    'GALLEY & CATERING', 'ACCOMMODATION', 'NAVIGATION', 'COMMUNICATION',
    'HULL & STRUCTURE', 'PUMPS & PIPES', 'TOOLS & WORKSHOP', 'CHEMICALS',
    'MAINTENANCE', 'SPARE PARTS', 'CONSUMABLES'
]

DESCRIPTIONS = [
    'BOLT, HEX HEAD, STAINLESS STEEL',
    'GASKET, RUBBER, ROUND',
    'VALVE, BALL, BRONZE',
    'WIRE, ELECTRICAL, COPPER',
    'BEARING, BALL, SEALED',
    'PUMP, CENTRIFUGAL, BRONZE',
    'FILTER, OIL, PAPER ELEMENT',
    'ROPE, POLYPROPYLENE, 12MM',
    'PAINT, MARINE, WHITE',
    'BULB, NAVIGATION, 12V'
]

def generate_products():
    """Generates a list of 51,425 product records."""
    print("Generating product data in memory...")
    products = []
    for i in range(1, 51426):
        code = str(i).zfill(6)
        description_base = random.choice(DESCRIPTIONS)
        description = f"{description_base} - {code}"
        category = random.choice(CATEGORIES)

        product = Product(
            impa_code=code,
            description=description,
            category=category
        )
        products.append(product)
    print("Product data generation complete.")
    return products

def main():
    """Main function to run the data ingestion."""
    with app.app_context():
        print("Data ingestion script started.")

        # Ensure the database tables are created
        print("Ensuring all database tables exist...")
        db.create_all()
        print("Tables created or already exist.")

        # Check if products already exist
        if db.session.query(Product).count() > 0:
            print("Products table is not empty. Deleting existing products to ensure a clean slate.")
            db.session.query(Product).delete()
            db.session.commit()
            print("Existing products deleted.")

        products_to_add = generate_products()

        print(f"Adding {len(products_to_add)} products to the database session in chunks...")

        # Add products in chunks to be memory-efficient
        chunk_size = 1000
        for i in range(0, len(products_to_add), chunk_size):
            chunk = products_to_add[i:i + chunk_size]
            db.session.bulk_save_objects(chunk)
            print(f"  - Added chunk {i // chunk_size + 1}/{(len(products_to_add) + chunk_size - 1) // chunk_size}")

        print("Committing all products to the database... This may take a few moments.")
        db.session.commit()
        print("Data ingestion complete! The database is now populated with product data.")

if __name__ == "__main__":
    main()
