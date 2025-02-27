import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.urls import reverse

from api.models import Cliente, ProdutoFavorito


@pytest.mark.django_db
def test_get_clientes_with_not_authentication():
    client = APIClient()

    response = client.get(reverse("cliente-list"))

    assert response.status_code == 401


@pytest.mark.django_db
def test_get_clientes_with_authentication(client_authenticated):
    response = client_authenticated.get(reverse("cliente-list"))

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_create_clientes(client_authenticated, cliente_data):
    response = client_authenticated.post(reverse("cliente-list"), data=cliente_data)
    data = response.json()

    assert response.status_code == 201
    assert data.get("email") == cliente_data.get("email")
    assert data.get("nome") == cliente_data.get("nome")

    response = client_authenticated.post(reverse("cliente-list"), data=cliente_data)
    assert response.status_code == 400
    assert response.json() == {'email': ['Cliente com este email já existe.']}


@pytest.mark.django_db
def test_delete_clientes(client_authenticated, cliente_data):
    response = client_authenticated.post(reverse("cliente-list"), data=cliente_data)
    assert response.status_code == 201
    
    cliente = Cliente.objects.get(email=response.json().get("email"))

    response = client_authenticated.delete(reverse("cliente-detail", kwargs={"pk": cliente.pk}))
    assert response.status_code == 204


@pytest.mark.django_db
def test_detail_clientes(client_authenticated, cliente_data):
    response = client_authenticated.post(reverse("cliente-list"), data=cliente_data)
    assert response.status_code == 201
    
    cliente = Cliente.objects.get(email=response.json().get("email"))

    response = client_authenticated.get(reverse("cliente-detail", kwargs={"pk": cliente.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_clientes(client_authenticated, cliente_data):
    response = client_authenticated.post(reverse("cliente-list"), data=cliente_data)
    assert response.status_code == 201
    
    cliente = Cliente.objects.get(email=response.json().get("email"))
    
    cliente_data["nome"] = "Novo nome"

    response = client_authenticated.put(reverse("cliente-detail", kwargs={"pk": cliente.pk}), data=cliente_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_partial_update_clientes(client_authenticated, cliente_data):
    response = client_authenticated.post(reverse("cliente-list"), data=cliente_data)
    assert response.status_code == 201
    
    cliente = Cliente.objects.get(email=response.json().get("email"))

    response = client_authenticated.patch(reverse("cliente-detail", kwargs={"pk": cliente.pk}), data={"email": "novo@novo.com"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_produtos_favoritos(client_authenticated):
    response = client_authenticated.get(reverse("produtofavorito-list"))

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
@patch("api.serializers.ProdutoFavoritoCreateSerializer.get_produto")
def test_create_produto_favorito(mock_get_produto, client_authenticated, produto_favorito_data, produto_api_data):
    mock_get_produto.return_value = produto_api_data

    response = client_authenticated.post(reverse("produtofavorito-list"), data=produto_favorito_data)
    data = response.json()

    assert response.status_code == 201
    assert data.get("email") == produto_favorito_data.get("email")
    assert data.get("id_produto") == produto_favorito_data.get("id_produto")

    response = client_authenticated.post(reverse("produtofavorito-list"), data=produto_favorito_data)
    assert response.status_code == 400
    assert response.json() == ["Produto já favoritado para o cliente selecionado."]


@pytest.mark.django_db
def test_create_produto_favorito_produto_nao_encontrado(client_authenticated, produto_favorito_data):
    produto_favorito_data["id_produto"] = 1
    response = client_authenticated.post(reverse("produtofavorito-list"), data=produto_favorito_data)
    
    assert response.status_code == 400
    assert response.json() == ["Não foi possível favoritar o produto. O produto não foi encontrato."]


@pytest.mark.django_db
def test_create_produto_favorito_cliente_nao_existe(client_authenticated, produto_favorito_data):
    produto_favorito_data["email"] = "teste@teste.com"
    response = client_authenticated.post(reverse("produtofavorito-list"), data=produto_favorito_data)
    
    assert response.status_code == 400
    assert response.json() == ["Cliente não encontrado."]


@pytest.mark.django_db
def test_filter_produto_favorito_de_cliente(client_authenticated, produto_favorito, produto_favorito_detail_data, cliente_data):
    cliente_data["email"] = "teste2@gmail.com"
    cliente = Cliente.objects.create(**cliente_data)
    produto_favorito_detail_data_new = produto_favorito_detail_data.copy()
    produto_favorito_detail_data_new["cliente"] = cliente
    del produto_favorito_detail_data_new["detalhe"]
    ProdutoFavorito(**produto_favorito_detail_data_new)

    response = client_authenticated.get(f"{reverse('produtofavorito-list')}?cliente__email={produto_favorito.cliente.email}")


    produto_favorito_detail_data["id"] = produto_favorito.pk
    
    assert response.status_code == 200
    assert response.json() == [produto_favorito_detail_data]


@pytest.mark.django_db
def test_delete_produto_favorito(client_authenticated, produto_favorito):
    response = client_authenticated.delete(reverse("produtofavorito-detail", kwargs={"pk": produto_favorito.pk}))
    assert response.status_code == 204
