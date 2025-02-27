# Desafio Tecnico Backend Wishlist LuizaLabs

API para salvar produtos favoritos de clientes
O desafio esta especificado no arquivo ([PDF] Desafio Tecnico Backend _ Wishlist _ LuizaLabs.pdf)

## Pré-requisitos

- Docker
- Docker compose


## Como usar

Em seu terminal execute:
```bash
docker compose build
docker compose up
```
Abra outro terminal e execute:
```bash
make create-super-user
```
Usuário criado será ``magalu`` e senha ``magalu``

Para rodar os testes:
```
make test
```



## Uso
A API utiliza-se de Basic authentication para realizar as requisições.

Você pode acessar diretamente a interface do django rest para realizar os testes no endpoint ```http://localhost:8000```

Ou fazer as requisições via postman ou outro programa de sua preferência.

## Área de clientes
**Criar cliente**
```
POST: http://localhost:8000/clientes/

Body:{
    "nome": "João",
    "email": "joao@teste.com"
}

Headers: {
    "Authorization": "Basic bWFnYWx1Om1hZ2FsdQ==" # Base64 do basic auth do usuário cadastrado
}

```
**Listar clientes**
```
GET: http://localhost:8000/clientes/

Headers: {
    "Authorization": "Basic bWFnYWx1Om1hZ2FsdQ==" # Base64 do basic auth do usuário cadastrado
}
```
**Detalhe do cliente**
```
GET: http://localhost:8000/clientes/{id}/

Headers: {
    "Authorization": "Basic bWFnYWx1Om1hZ2FsdQ==" # Base64 do basic auth do usuário cadastrado
}
```
**Atualizar um cliente**
```
PUT: http://localhost:8000/clientes/{id}/

Body:{
    "nome": "Maria",
    "email": "maria@teste.com"
}

Headers: {
    "Authorization": "Basic bWFnYWx1Om1hZ2FsdQ==" # Base64 do basic auth do usuário cadastrado
}
```

**Atualizar parcialmente um cliente**
```
PATCH: http://localhost:8000/clientes/{id}/

Body:{
    "nome": "Maria"
}

Headers: {
    "Authorization": "Basic bWFnYWx1Om1hZ2FsdQ==" # Base64 do basic auth do usuário cadastrado
}
```

**Remover cliente**
```
DELETE: http://localhost:8000/clientes/{id}/

Headers: {
    "Authorization": "Basic bWFnYWx1Om1hZ2FsdQ==" # Base64 do basic auth do usuário cadastrado
}
```

## Área de Produtos Favoritos
A listagem de produtos se encontra em uma API publica onde pode se consultar quais são os produtos disponíveis: ``https://api.escuelajs.co/api/v1/products/``

**Favoritar um produto**
```
POST: http://localhost:8000/produtos-favoritos/

Body: {
    "email": "joao@teste.com",
    "id_produto: 5 # Id do produto na API terceira mencionada acima
}

Headers: {
    "Authorization": "Basic bWFnYWx1Om1hZ2FsdQ==" # Base64 do basic auth do usuário cadastrado
}
```
**Listar todos os produtos favoritos de todos os clientes**
```
GET: http://localhost:8000/produtos-favoritos/

Headers: {
    "Authorization": "Basic bWFnYWx1Om1hZ2FsdQ==" # Base64 do basic auth do usuário cadastrado
}
```

**Listar todos os produtos favoritos de um cliente especifico**
```
GET: http://localhost:8000/produtos-favoritos/?cliente__email=joao@teste.com

Headers: {
    "Authorization": "Basic bWFnYWx1Om1hZ2FsdQ==" # Base64 do basic auth do usuário cadastrado
}
```

**Remover um produto de um favorito**
```
DELETE: http://localhost:8000/produtos-favoritos/{id}/
# {id} corresponte ao id produto favorito e não ao id_produto

Headers: {
    "Authorization": "Basic bWFnYWx1Om1hZ2FsdQ==" # Base64 do basic auth do usuário cadastrado
}
```
