import requests

from django.urls import reverse
from rest_framework import serializers
from django.conf import settings

from .models import Cliente, ProdutoFavorito
    

class ProdutoFavoritoDetailSerializer(serializers.ModelSerializer):
    detalhe = serializers.SerializerMethodField(source="get_detalhe")

    class Meta:
        model = ProdutoFavorito
        fields = [
            'id',
            'cliente',
            'titulo',
            'imagem',
            'preco',
            'id_produto',
            'detalhe',
        ]

    def get_detalhe(self, obj):
        return settings.API_PRODUCTS_URL + str(obj.id_produto)


class ProdutoFavoritoCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    
    class Meta:
        model = ProdutoFavorito
        fields = [
            'email',
            'id_produto',
        ]


    def get_produto(self, id_produto):
        response = requests.get(settings.API_PRODUCTS_URL + str(id_produto))
        if response.status_code != 200:
            raise serializers.ValidationError("Não foi possível favoritar o produto. O produto não foi encontrato.")
        
        return response.json()

    def create(self, validated_data):
        email = validated_data["email"]
        id_produto = validated_data["id_produto"]
        
        try:
            cliente = Cliente.objects.get(email=email)
        except Cliente.DoesNotExist:
            raise serializers.ValidationError("Cliente não encontrado.")
        
        data_produto = self.get_produto(id_produto)

        if ProdutoFavorito.objects.filter(cliente=cliente, id_produto=id_produto).exists():
            raise serializers.ValidationError("Produto já favoritado para o cliente selecionado.")

        cliente = ProdutoFavorito.objects.create(
            cliente=cliente,
            id_produto=id_produto,
            preco=data_produto.get("price"),
            titulo=data_produto.get("title"),
            imagem=data_produto.get("images")[0][:200]
        )
        return validated_data


class ClienteSerializer(serializers.ModelSerializer):
    produtos_favoritos = ProdutoFavoritoDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', "produtos_favoritos"]
