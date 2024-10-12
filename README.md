# H&T Handcraft: Final Project for SDA Python Course "PythonRemoteEE23"

### Overview  
H&T Handcraft is an e-shop platform designed to sell handcrafted products. It allows users to search for products, add them to the cart, and complete the checkout process smoothly.

---

### Technologies Used  
- **IDE**: PyCharm 2023.2.3 (Professional Edition)  
- **Language**: Python 3.12.0  
- **Framework**: Django 5.1.1  
- **Database**: PostgreSQL 16.4  

---

### Installation Steps  

1. **Clone the repository**:  
    ```bash  
    git clone https://github.com/m6mmi/h-t-handcraft  
    cd h-t-handcraft  
    ```  

2. **Install dependencies**:  
    ```bash  
    pip install -r requirements.txt  
    ```  

3. **Create a virtual environment**:  
    ```bash  
    python -m venv venv  
    source venv/bin/activate  # On Windows: venv\Scripts\activate  
    ```  

4. **Install project dependencies**:  
    ```bash  
    pip install -r requirements.txt  
    ```  

5. **Configure the environment**:  
    ```bash  
    cp .env.example .env  
    ```  

6. **Set up the database**:  
    - Ensure PostgreSQL is installed and running.  
    - Create a database named `h_t_handcraft`.  
    - Update the `.env` file with your PostgreSQL credentials. (See example.env file)

7. **Run the development server**:  
    ```bash  
    python manage.py runserver  
    ```

---

### Product Import via CSV  
Products can be imported to the e-shop by running the script `import_csv.py`. Example CSV file: `ht_products.csv`.

---

### Features  

- **Class-Based Views (CBVs)**:  
  Extensive use of Django's generic views (`ListView`, `DetailView`, `TemplateView`, etc.) for product listings, details, and static pages.  
- **Custom Views**:  
  Custom views such as `IndexView` for the homepage and `AddToCart` for managing the cart.  
- **Authentication**:  
  `LoginRequiredMixin` is used to restrict certain views to authenticated users.  
- **Pagination**:  
  Pagination is used in product listings, with random product selection for the homepage to enhance the user experience.

---

### Testing  

To run the tests, use the following command:  
```bash  
pytest products/tests.py  

```


### Credits
This project is a collaboration by:

- Janek Sitsmann
- Triinu Niklus
- Indrek Kuusk