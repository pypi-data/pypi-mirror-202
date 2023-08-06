```
# MagPy

MagPy é uma API REST desenvolvida com Flask que gerencia uma coleção de projetos. Cada projeto tem um nome e uma lista de pacotes. Cada pacote tem um nome e uma versão.

## Instalação

Para instalar as dependências necessárias para executar este projeto, execute o seguinte comando em seu terminal:

```
pip install flask requests
```

## Uso

Para executar a API localmente, execute o seguinte comando em seu terminal:

```
python app.py
```

Isso iniciará a API na porta 5000. Você pode acessar a API em `http://localhost:5000`.

A API tem as seguintes rotas disponíveis:

### POST /api/projects

Cria um novo projeto. O corpo da solicitação deve ter o seguinte formato:

```json
{
    "name": "titan",
    "packages": [
        {"name": "Django"},
        {"name": "graphene", "version": "2.0"}
    ]
}
```

Onde `name` é o nome do projeto e `packages` é uma lista de pacotes. Cada pacote deve ter um `name` e pode opcionalmente ter uma `version`. Se nenhuma versão for especificada para um pacote, a API usará a versão mais recente do pacote disponível no PyPI.

Se a solicitação for bem-sucedida, a API retornará uma resposta com o código de status HTTP 201 e os dados do projeto criado no corpo da resposta.

Se algum dos pacotes especificados não existir ou se alguma das versões especificadas for inválida, a API retornará um erro com o código de status HTTP 400.

### GET /api/projects/<project_name>

Recupera os dados de um projeto previamente criado. Substitua `<project_name>` pelo nome do projeto que deseja recuperar.

Se o projeto existir, a API retornará uma resposta com o código de status HTTP 200 e os dados do projeto no corpo da resposta.

Se o projeto não existir, a API retornará um erro com o código de status HTTP 404.

### DELETE /api/projects/<project_name>

Exclui um projeto previamente criado. Substitua `<project_name>` pelo nome do projeto que deseja excluir.

Se o projeto existir, a API excluirá o projeto e retornará uma resposta vazia com o código de status HTTP 204.

Se o projeto não existir, a API retornará um erro com o código de status HTTP 404.
```