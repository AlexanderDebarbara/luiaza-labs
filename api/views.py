from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cliente, ProdutoFavorito
from .serializers import ClienteSerializer, ProdutoFavoritoCreateSerializer, ProdutoFavoritoDetailSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ProdutoFavoritoViewSet(viewsets.ModelViewSet):
    queryset = ProdutoFavorito.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cliente__email']
    http_method_names = ["get", "post", "delete"]

    def get_serializer_class(self):
        if self.action == "create":
            return ProdutoFavoritoCreateSerializer
        return ProdutoFavoritoDetailSerializer
