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

## Decisões de implementação

As tecnologias principais foram definidas pelo próprio desafio. Durante a implementação, algumas decisões foram tomadas para manter a solução simples e segura dentro do prazo.

A autenticação utiliza Token Authentication do Django REST Framework, atendendo ao requisito de proteção da API sem adicionar complexidade desnecessária. Staging e produção foram mantidos em ambientes e bancos separados para evitar que testes afetem os dados de produção. As configurações sensíveis são fornecidas por variáveis de ambiente, enquanto o Docker mantém a execução consistente entre desenvolvimento, CI e AWS.

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

### Regras de agendamento

Para evitar inconsistências, a API aplica algumas regras de negócio às consultas:

- consultas só podem ser agendadas para datas futuras;
- um mesmo profissional não pode possuir duas consultas no mesmo horário;
- profissionais diferentes podem possuir consultas no mesmo horário.

A prevenção de conflito é aplicada tanto na validação da API quanto por uma constraint no banco de dados.

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

Para execução local sem Docker, é necessário ter uma instância do PostgreSQL em execução e configurar no `.env` as credenciais correspondentes.

Para uma configuração mais rápida e reproduzível, recomenda-se utilizar o Docker Compose descrito na seção seguinte.

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

Também é possível executar o projeto utilizando Docker.

Primeiro, crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

No PowerShell:

```markdown
```powershell
Copy-Item .env.example .env
```

Depois execute:

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

Atualmente a suíte possui 25 testes automatizados, cobrindo:

- CRUD de profissionais;
- CRUD de consultas;
- autenticação;
- filtros por profissional;
- cenários de erro;
- validações de nome, profissão, endereço e contato;
- contatos por e-mail e telefone;
- bloqueio de consultas no passado;
- prevenção de conflito de horário;
- possibilidade de profissionais diferentes utilizarem o mesmo horário.

Para executar:

```bash
poetry run python manage.py test
```

Com Docker:

```bash
docker compose run --rm --entrypoint python web manage.py test
```

Para verificar a cobertura:

```bash
poetry run coverage run --source=professionals,appointments manage.py test
poetry run coverage report -m
```

O pipeline exige cobertura mínima de 90%.

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

Mais detalhes sobre os ambientes, o fluxo real de implantação e as evidências de deploy estão disponíveis em:

[Documentação de Deploy](docs/DEPLOYMENT.md)

## CI/CD

O projeto utiliza GitHub Actions.

O workflow está versionado em:

`.github/workflows/ci.yml`

As execuções podem ser consultadas publicamente em:

https://github.com/Iverzada/lacrei-api/actions

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

O Elastic Beanstalk mantém versões anteriores da aplicação, permitindo restaurar uma versão estável caso um novo deploy apresente problemas.

As versões são identificadas pelo SHA do commit, permitindo relacionar cada deploy ao código correspondente no GitHub.

O procedimento completo de rollback, incluindo identificação da versão estável, comandos AWS CLI, validação pós-rollback e evidência do teste realizado em staging, está documentado em:

[Procedimento de Rollback](docs/ROLLBACK.md)

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
