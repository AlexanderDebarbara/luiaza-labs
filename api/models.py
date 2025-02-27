from django.db import models

class Cliente(models.Model):
    nome = models.CharField("nome", max_length=255)
    email = models.EmailField("email", max_length=254, unique=True)    

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.email
    

class ProdutoFavorito(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='produtos_favoritos', on_delete=models.CASCADE)
    titulo = models.CharField("titulo", max_length=50)
    imagem = models.URLField("imagem", max_length=200)
    preco = models.DecimalField("preco", max_digits=5, decimal_places=2)
    id_produto = models.IntegerField("ID produto")

    class Meta:
        verbose_name = "Produto Favorito"
        verbose_name_plural = "Produtos Favoritos"
        unique_together = [['cliente', 'id_produto']]

    def __str__(self):
        return self.titulo

