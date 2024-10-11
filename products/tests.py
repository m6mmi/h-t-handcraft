import pytest
from products.models import Product, Category


@pytest.mark.django_db
def test_create_product():
    # Create a category
    category = Category.objects.create(name="Kassid")

    # Create a product
    product = Product.objects.create(
        title="Kuri kass",
        description="Kuri kass",
        price=7,
        stock=5,
        category=category,
        height=0.5,
        width=3.0,
        length=6.5,
        weight=0.4,
    )

    # Check if product is created successfully
    assert product.id is not None
    assert product.title == "Kuri kass"


@pytest.mark.django_db
def test_read_product():
    # Create a category
    category = Category.objects.create(name="Kassid")

    # Create and save a product
    product = Product.objects.create(
        title="Kuri kass",
        description="Kuri kass",
        price=7,
        stock=9,
        category=category,
    )

    # Retrieve the product
    retrieved_product = Product.objects.get(id=product.id)

    # Check if the retrieved product matches the original one
    assert retrieved_product.title == "Kuri kass"
    assert retrieved_product.price == 7


@pytest.mark.django_db
def test_update_product():
    # Create a category
    category = Category.objects.create(name="Kassid")

    # Create a product
    product = Product.objects.create(
        title="Eriti kuri kass",
        description="Eriti kuri kass",
        price=13,
        stock=2,
        category=category,
    )

    # Update the product
    product.price = 13
    product.stock = 2
    product.save()

    # Fetch the updated product from the database
    updated_product = Product.objects.get(id=product.id)

    # Check if the product details have been updated
    assert updated_product.price == 13
    assert updated_product.stock == 2


@pytest.mark.django_db
def test_delete_product():
    # Create a category
    category = Category.objects.create(name="Kassid")

    # Create a product
    product = Product.objects.create(
        title="Kuri kass",
        description="Kuri kass",
        price=13,
        stock=7,
        category=category,
    )

    # Delete the product
    product.delete()

    # Check if the product no longer exists in the database
    with pytest.raises(Product.DoesNotExist):
        Product.objects.get(id=product.id)


@pytest.mark.django_db
def test_list_products():
    # Create a category
    category = Category.objects.create(name="Kassid_3")

    # Create multiple products
    Product.objects.create(title="Puust piimakauss kassile", description="Puust piimakauss kassile kaunistustega", price=18, stock=9, category=category)
    Product.objects.create(title="Purõja pini", description="Purõja pini, kae perra tulõ õkva su mano!", price=19, stock=7, category=category)

    # Retrieve all products
    products = Product.objects.all()

    # Check if the number of products is correct
    assert len(products) == 2
