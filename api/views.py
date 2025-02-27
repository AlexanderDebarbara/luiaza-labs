from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cliente, ProdutoFavorito
from .serializers import ClienteSerializer, ProdutoFavoritoCreateSerializer, ProdutoFavoritoDetailSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ProdutoFavoritoViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ProdutoFavorito.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cliente__email']

    def get_serializer_class(self):
        if self.action == "create":
            return ProdutoFavoritoCreateSerializer
        return ProdutoFavoritoDetailSerializer
