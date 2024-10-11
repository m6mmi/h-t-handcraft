"H&T Handcraft" is our SDA Python course "PythonRemoteEE23" final project.

This project was made to sell handcraft products from e-shop. The user can search products, add products to cart and checkout.


Technology

This project is based on:

PyCharm 2023.2.3 (Professional Edition) / Python 3.12.0

Django 5.1.1

PostgreSQL 16.4

Installation

    Clone the repository:

    git clone  https://github.com/m6mmi/h-t-handcraft cd h-t-handcraft

    Install the project dependencies:

    pip install -r requirements.txt

    Create a virtual environment and install dependencies:

    python -m venv venv

    source venv/bin/activate # On Windows: venv\Scripts\activate

    pip install -r requirements.txt

    Copy the example environment file:

    cp .env.example .env

    Database Setup

    Ensure PostgreSQL is installed and running.

    Create a PostgreSQL database named h_t_handcraft.

    Update the database configuration in .env with your PostgreSQL credentials

    Start the development server

    python manage.py runserver


Products can be imported to e-shop by script via CSV file import_csv.py example file  ht_products.csv

In this project, we utilize Class-Based Views (CBVs) extensively, including Django's generic views such as 
ListView, DetailView, and TemplateView. These provide an organized and reusable way to handle typical operations 
such as listing products, showing product details, and rendering static pages. Additionally, we use custom 
class-based views for specific functionalities like the homepage (IndexView) and the cart management (AddToCart). 
LoginRequiredMixin is employed to restrict access to authenticated users, ensuring certain views are protected. 
Pagination is implemented in product listing views, and random product selection is used for the homepage 
to enhance the user experience.

Testing

To test code go tests.py and run  "pytest products/tests.py"

Credits

This project was made as a collaboration by:

Janek Sitsmann
Triinu Niklus
Indrek Kuusk
