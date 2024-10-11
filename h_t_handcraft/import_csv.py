import csv
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'h_t_handcraft.settings')
django.setup()

from products.models import Product, Category

# Path to the CSV file
CSV_FILE_PATH = '../ht_products.csv'


# Function to add products to the database
def add_products_from_csv(file_path):
    with open(file_path, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        # Clean the headers to remove leading/trailing spaces
        reader.fieldnames = [header.strip() for header in reader.fieldnames]
        print("Cleaned Headers:", reader.fieldnames)  # Debug: Print cleaned headers to confirm correct reading

        for row in reader:
            # Strip spaces from each key in the row dictionary
            row = {key.strip(): value for key, value in row.items()}

            try:
                # Extract and validate fields from the CSV row
                title = row['title']
                description = row.get('description', '')  # Default to empty string if missing

                # Validate and convert price
                price_str = row['price']
                try:
                    price = float(price_str)
                except ValueError:
                    print(f"Skipping row due to invalid price: {price_str}")
                    continue  # Skip this row

                # Validate and convert stock
                stock_str = row['stock']
                if not stock_str.isdigit():
                    print(f"Skipping row due to invalid stock value: {stock_str}")
                    continue  # Skip this row

                stock = int(stock_str)

                # Extract subcategory name
                subcategory_name = row['category']  # Changed from category to subcategory

                # Extract additional fields
                image_path = row.get('image_path', '')
                height = float(row.get('height', 0)) if row.get('height') else None
                width = float(row.get('width', 0)) if row.get('width') else None
                length = float(row.get('lenght', 0)) if row.get('lenght') else None  # Spelling corrected in the CSV as well
                weight = float(row.get('weight', 0)) if row.get('weight') else None

                # Get or create the subcategory (assuming Category is used as subcategory)
                category, created = Category.objects.get_or_create(name=subcategory_name)

                # Create or update the product
                product, created = Product.objects.get_or_create(
                    title=title,
                    defaults={
                        'description': description,
                        'price': price,
                        'stock': stock,
                        'category': category,  # Make sure to use 'category' instead of 'subcategory'
                        'image_path': image_path,
                        'height': height,
                        'width': width,
                        'length': length,
                        'weight': weight,
                    }
                )

                if created:
                    print(f"Product '{title}' added successfully.")
                else:
                    print(f"Product '{title}' already exists, updating existing product.")
                    # If the product already exists, you can choose to update fields if needed:
                    product.description = description
                    product.price = price
                    product.stock = stock
                    product.category = category
                    product.image_path = image_path
                    product.height = height
                    product.width = width
                    product.length = length
                    product.weight = weight
                    product.save()

            except KeyError as e:
                print(f"KeyError: {e} in row {row}")
                continue


# Run the function
if __name__ == '__main__':
    add_products_from_csv(CSV_FILE_PATH)
