import pytest
from products.models import Product, Category, Subcategory

@pytest.fixture
def category():
    return Category.objects.create(name="Reeglid")

@pytest.fixture
def subcategory(category):
    return Subcategory.objects.create(name="Saun", category=category)

@pytest.fixture
def product(subcategory):
    return Product.objects.create(
        title="Kui on must",
        description="Kui on must",
        price=12.00,
        stock=2,
        subcategory=subcategory
    )

# Create Test
@pytest.mark.django_db
def test_create_product(subcategory):
    product = Product.objects.create(
        title="Uus toode",
        description="Uus toode kirjeldus",
        price=29.99,
        stock=5,
        subcategory=subcategory
    )
    assert product.title == "Uus toode"
    assert product.price == 29.99
    assert product.stock == 5

# Read Test
@pytest.mark.django_db
def test_read_product(product):
    fetched_product = Product.objects.get(id=product.id)
    assert fetched_product.title == "Uus toode"
    assert fetched_product.description == "Uus toode"
    assert fetched_product.price == 19.99

# Update Test
@pytest.mark.django_db
def test_update_product(product):
    product.title = "Uus toode, uuendatud"
    product.price = 24.99
    product.save()

    updated_product = Product.objects.get(id=product.id)
    assert updated_product.title == "Uus toode, uuendatud"
    assert updated_product.price == 24.99

# Delete Test
@pytest.mark.django_db
def test_delete_product(product):
    product_id = product.id
    product.delete()

    with pytest.raises(Product.DoesNotExist):
        Product.objects.get(id=product_id)

# List All Products Test
@pytest.mark.django_db
def test_list_products(product, subcategory):
    products = Product.objects.all()
    assert len(products) == 1  # Since we only created one product in the fixture

