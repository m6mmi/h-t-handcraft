from .models import Category


def categories(request):
    print("Categories context processor called")
    return {'categories': Category.objects.all()}
