from market.models import Kategori


def kategorite(request):
    return {'kategorite': Kategori.objects.all()}
