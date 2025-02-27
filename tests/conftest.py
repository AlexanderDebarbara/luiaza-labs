import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient

from api.models import Cliente, ProdutoFavorito

@pytest.fixture(autouse=True)
@pytest.mark.django_db
def user():
    User.objects.create_superuser('magalu', 'magalu@magalu.com', 'magalu')


@pytest.fixture
def client_authenticated():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Basic bWFnYWx1Om1hZ2FsdQ==')

    return client


@pytest.fixture
def cliente_data():
    return {
        "nome": "Alexander Debarbara",
        "email": "debarbara4@gmail.com"
    }


@pytest.fixture
@pytest.mark.django_db
def cliente(cliente_data):
    return Cliente.objects.create(**cliente_data)


@pytest.fixture
def produto_api_data():
    return {
        "title": "Classic Grey Hooded Sweatshirt",
        "images": ["https://i.imgur.com/R2PN9Wq.jpeg"],
        "price": "98.00",
    }


@pytest.fixture
def produto_favorito_data(cliente):
    return {
        "email": cliente.email,
        "id_produto": 4
    }


@pytest.fixture
def produto_favorito_complete_data(cliente):
    return {
        "cliente": cliente,
        "titulo": "Classic Grey Hooded Sweatshirt",
        "imagem": "https://i.imgur.com/R2PN9Wq.jpeg",
        "preco": "98.00",
        "id_produto": 4,
    }


@pytest.fixture
@pytest.mark.django_db
def produto_favorito(produto_favorito_complete_data):
    return ProdutoFavorito.objects.create(**produto_favorito_complete_data)


@pytest.fixture
def produto_favorito_detail_data(produto_favorito_complete_data, cliente):
    produto_favorito_complete_data["cliente"] = cliente.pk
    produto_favorito_complete_data["detalhe"] = 'https://api.escuelajs.co/api/v1/products/4'

    return produto_favorito_complete_data
