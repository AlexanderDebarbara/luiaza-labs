from rest_framework import routers

from .views import ClienteViewSet, ProdutoFavoritoViewSet

router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos-favoritos', ProdutoFavoritoViewSet)
