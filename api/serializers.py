import requests

from django.urls import reverse
from rest_framework import serializers
from django.conf import settings

from .models import Cliente, ProdutoFavorito


class ClienteSerializer(serializers.ModelSerializer):
    detalhe = serializers.SerializerMethodField(source="get_detalhe")

    class Meta:
        model = Cliente
        fields = ['nome', 'email', "detalhe"]

    def get_detalhe(self, obj):
        return reverse("cliente-detail", kwargs={'pk': obj.pk})
    

class ProdutoFavoritoDetailSerializer(serializers.ModelSerializer):
    detalhe = serializers.SerializerMethodField(source="get_detalhe")

    class Meta:
        model = ProdutoFavorito
        fields = [
            'cliente_id',
            'titulo',
            'imagem',
            'preco',
            'id_produto',
            'detalhe',
        ]

    def get_detalhe(self, obj):
        return settings.API_PRODUCTS_URL + str(obj.id_produto)


class ProdutoFavoritoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutoFavorito
        fields = [
            'cliente',
            'id_produto',
        ]

    def create(self, validated_data):
        cliente = validated_data["cliente"]
        id_produto = validated_data["id_produto"]

        response = requests.get(settings.API_PRODUCTS_URL + str(id_produto))
        if response.status_code != 200:
            raise serializers.ValidationError("Não foi possível favoritar o produto. O produto não foi encontrato.")
        
        data_produto = response.json()

        cliente = ProdutoFavorito.objects.create(
            cliente=cliente,
            id_produto=id_produto,
            preco=data_produto.get("price"),
            titulo=data_produto.get("title"),
            imagem=data_produto.get("images")[0]            
        )
        return cliente
