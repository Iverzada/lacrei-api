# Lacrei Saúde API

API REST desenvolvida para o desafio técnico da Lacrei Saúde.

O projeto permite cadastrar e gerenciar profissionais de saúde e consultas médicas. Além do CRUD completo, foram implementados autenticação, validação dos dados, testes automatizados, documentação Swagger, Docker e deploy na AWS com ambientes separados de staging e produção.

## Tecnologias

As principais tecnologias utilizadas, seguindo os requisitos do desafio, foram:

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- Poetry
- Docker
- GitHub Actions
- AWS Elastic Beanstalk
- AWS RDS
- Ruff
- Coverage
- Swagger / OpenAPI

## Funcionalidades

### Profissionais

A API permite:

- cadastrar profissionais;
- listar profissionais;
- buscar por ID;
- atualizar;
- atualizar parcialmente;
- excluir.

Cada profissional possui:

```text
nome social
profissão
endereço
contato
```

### Consultas

Também é possível:

- cadastrar consultas;
- listar consultas;
- buscar por ID;
- atualizar;
- excluir;
- buscar consultas pelo profissional responsável.

Exemplo:

```http
GET /api/v1/appointments/?profissional=1
```

### Autenticação

```text
POST /api/v1/auth/token/
```

Depois de gerar o token, ele deve ser enviado no header:

```http
Authorization: Token SEU_TOKEN
```

## Documentação

A API possui documentação interativa com Swagger e ReDoc.

```text
Swagger: /api/docs/
ReDoc:   /api/redoc/
Schema:  /api/schema/
```

Pelo Swagger é possível autenticar e testar os endpoints diretamente pelo navegador.

## Executando localmente

Clone o projeto:

```bash
git clone https://github.com/Iverzada/lacrei-api.git
cd lacrei-api
```

Instale as dependências:

```bash
poetry install
```

Crie um `.env` usando o `.env.example` como referência.

Depois execute:

```bash
poetry run python manage.py migrate
poetry run python manage.py runserver
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

## Docker

Também é possível executar o projeto utilizando Docker:

```bash
docker compose up --build
```

A API ficará disponível em:

```text
http://localhost:8000
```

Para encerrar:

```bash
docker compose down
```

## Testes

Os testes foram desenvolvidos utilizando `APITestCase` do Django REST Framework.

Eles cobrem o CRUD de profissionais e consultas, autenticação, filtros e cenários de erro.

Para executar:

```bash
poetry run python manage.py test
```

Para verificar a cobertura:

```bash
poetry run coverage run --source=professionals,appointments manage.py test
poetry run coverage report -m
```

Durante o desenvolvimento, a cobertura ficou em aproximadamente **97%**.

O pipeline exige pelo menos **90%**.

Para verificar o código com Ruff:

```bash
poetry run ruff check .
```

## Segurança

A API utiliza autenticação por token e todos os endpoints de profissionais e consultas são protegidos.

Os dados recebidos passam pelos serializers antes de serem salvos e os campos possuem validações para impedir valores inválidos ou vazios.

O acesso ao PostgreSQL é feito utilizando o ORM do Django, evitando consultas SQL construídas diretamente com dados enviados pelo usuário.

O CORS também é configurado por variável de ambiente, permitindo configurações diferentes para desenvolvimento, staging e produção.

Credenciais e chaves não são armazenadas no repositório.

## Deploy

A aplicação está hospedada na AWS em dois ambientes separados:

```text
Staging
Elastic Beanstalk: lacrei-amb
PostgreSQL: AWS RDS

Produção
Elastic Beanstalk: lacrei-prod
PostgreSQL: AWS RDS
```

Os bancos de staging e produção são separados e não possuem acesso público.

## CI/CD

O projeto utiliza GitHub Actions.

A cada push na branch `main`, o pipeline executa:

```text
Lint
  ↓
Testes
  ↓
Cobertura
  ↓
Docker Build
  ↓
Deploy Staging
  ↓
Deploy Produção
```

O deploy só acontece se as etapas anteriores forem concluídas com sucesso.

Cada versão enviada para a AWS utiliza o SHA do commit no nome, facilitando identificar qual versão do código está em execução.

## Rollback

O Elastic Beanstalk mantém as versões anteriores da aplicação.

Caso uma nova versão apresente problemas, é possível localizar a última versão estável e implantá-la novamente.

Como as versões usam o SHA do commit:

```text
github-<SHA_DO_COMMIT>
```

é possível relacionar facilmente cada deploy ao código correspondente no GitHub.

O rollback também pode ser feito pela AWS CLI:

```bash
aws elasticbeanstalk update-environment \
  --environment-name NOME_DO_AMBIENTE \
  --version-label github-SHA_ESTAVEL
```

## Possível integração com Asaas

Como melhoria futura, a API poderia utilizar o Asaas para gerar cobranças relacionadas às consultas.

Um fluxo possível seria:

```text
Consulta criada
      ↓
Cobrança criada no Asaas
      ↓
Pagamento realizado
      ↓
Webhook enviado para a API
      ↓
Status do pagamento atualizado
```

A integração ficaria isolada em um serviço próprio, evitando misturar a lógica de pagamentos com o gerenciamento das consultas.

A chave da API do Asaas seria armazenada como variável de ambiente e nunca diretamente no código.