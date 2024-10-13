import pytest
from products.models import Product, Category


@pytest.mark.django_db
def test_create_product():
    category = Category.objects.create(name="Kassid")
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

    assert product.id is not None
    assert product.title == "Kuri kass"


@pytest.mark.django_db
def test_read_product():
    category = Category.objects.create(name="Kassid")
    product = Product.objects.create(
        title="Kuri kass",
        description="Kuri kass",
        price=7,
        stock=9,
        category=category,
    )
    retrieved_product = Product.objects.get(id=product.id)

    assert retrieved_product.title == "Kuri kass"
    assert retrieved_product.price == 7


@pytest.mark.django_db
def test_update_product():
    category = Category.objects.create(name="Kassid")
    product = Product.objects.create(
        title="Eriti kuri kass",
        description="Eriti kuri kass",
        price=13,
        stock=2,
        category=category,
    )
    product.price = 13
    product.stock = 2
    product.save()
    updated_product = Product.objects.get(id=product.id)

    assert updated_product.price == 13
    assert updated_product.stock == 2


@pytest.mark.django_db
def test_delete_product():
    category = Category.objects.create(name="Kassid")
    product = Product.objects.create(
        title="Kuri kass",
        description="Kuri kass",
        price=13,
        stock=7,
        category=category,
    )
    product.delete()
    with pytest.raises(Product.DoesNotExist):
        Product.objects.get(id=product.id)


@pytest.mark.django_db
def test_list_products():
    category = Category.objects.create(name="Kassid_3")
    Product.objects.create(
        title="Puust piimakauss kassile",
        description="Puust piimakauss kassile kaunistustega",
        price=18,
        stock=9,
        category=category
    )
    Product.objects.create(
        title="Purõja pini",
        description="Purõja pini, kae perra tulõ õkva su mano!",
        price=19,
        stock=7,
        category=category
    )
    products = Product.objects.all()

    assert len(products) == 2
