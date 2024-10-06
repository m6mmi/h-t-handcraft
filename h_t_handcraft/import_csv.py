import csv
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'h_t_handcraft.settings')
django.setup()

from products.models import Product, Subcategory

# Path to the CSV file
CSV_FILE_PATH = '../ht_products7.csv'



# Function to add products to the database
def add_products_from_csv(file_path):
    with open(file_path, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        print("Headers:", reader.fieldnames)  # Debug: Print headers to confirm correct reading

        for row in reader:
            try:
                # Extract and validate fields from the CSV row
                title = row['Title']
                description = row['Description']

                # Validate and convert price
                price_str = row['Price']
                try:
                    price = float(price_str)
                except ValueError:
                    print(f"Skipping row due to invalid price: {price_str}")
                    continue  # Skip this row

                # Validate and convert stock
                stock_str = row['Stock']
                if not stock_str.isdigit():
                    print(f"Skipping row due to invalid stock value: {stock_str}")
                    continue  # Skip this row

                stock = int(stock_str)
                subcategory_name = row['Subcategory']

                # Get or create the subcategory
                subcategory, created = Subcategory.objects.get_or_create(name=subcategory_name)

                # Create the product
                product, created = Product.objects.get_or_create(
                    title=title,
                    defaults={
                        'description': description,
                        'price': price,
                        'stock': stock,
                        'subcategory': subcategory,
                    }
                )

                if created:
                    print(f"Product '{title}' added successfully.")
                else:
                    print(f"Product '{title}' already exists.")

            except KeyError as e:
                print(f"KeyError: {e} in row {row}")
                continue


# Run the function
if __name__ == '__main__':
    add_products_from_csv(CSV_FILE_PATH)
