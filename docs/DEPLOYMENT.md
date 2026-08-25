# Deploy da aplicação

A API possui ambientes separados de staging e produção, hospedados na AWS utilizando Elastic Beanstalk e PostgreSQL no Amazon RDS.

## Ambientes

### Staging

Documentação Swagger:

http://lacrei-amb.eba-ssmpxt2b.us-east-2.elasticbeanstalk.com/api/docs/

O ambiente de staging é utilizado para validar a aplicação antes da promoção para produção.

### Produção

Documentação Swagger:

http://lacrei-prod.eba-exshdvpe.us-east-2.elasticbeanstalk.com/api/docs/

O ambiente de produção é atualizado somente após a conclusão bem-sucedida das etapas de qualidade e do deploy em staging.

## Fluxo de CI/CD

O processo de integração e entrega contínua é executado pelo GitHub Actions através do workflow:

`.github/workflows/ci.yml`

A esteira executa, nesta ordem:

1. Instalação das dependências com Poetry.
2. Análise estática utilizando Ruff.
3. Validação do projeto com `manage.py check`.
4. Execução dos testes automatizados.
5. Verificação da cobertura mínima de 90%.
6. Build da imagem Docker.
7. Deploy no ambiente de staging.
8. Validação da versão implantada em staging.
9. Deploy da mesma versão no ambiente de produção.
10. Validação da versão implantada em produção.

Caso alguma etapa anterior falhe, as etapas seguintes não são executadas.

## GitHub Actions

Os workflows podem ser acompanhados publicamente em:

https://github.com/Iverzada/lacrei-api/actions

Exemplo de execução completa da esteira:

https://github.com/Iverzada/lacrei-api/actions/runs/32867431450

Nesta execução foram concluídos com sucesso:

- `lint-test-build`
- `Deploy staging`
- `Deploy production`

## Versionamento do deploy

Cada deploy utiliza como identificador:

`github-<GITHUB_SHA>`

Dessa forma, a versão implantada na AWS pode ser associada diretamente ao commit que originou aquele deploy.

O mesmo artefato validado em staging é utilizado para criar a versão correspondente da aplicação de produção, reduzindo diferenças entre os dois ambientes.

## Infraestrutura

O fluxo simplificado da aplicação é:

GitHub  
→ GitHub Actions  
→ testes, lint e build  
→ AWS Elastic Beanstalk (staging)  
→ AWS Elastic Beanstalk (produção)  
→ Amazon RDS PostgreSQL

As configurações sensíveis, como credenciais do banco de dados e chaves da AWS, não são armazenadas no código-fonte.

As credenciais utilizadas pelo GitHub Actions são armazenadas como GitHub Actions Secrets, enquanto as configurações da aplicação são fornecidas através das variáveis de ambiente dos ambientes da AWS.

## Evidência de implantação

A versão implantada pode ser consultada diretamente pela AWS CLI e foi validada diretamente na AWS.

### Staging

- Status: Ready
- Health: Green
- VersionLabel: github-452dc274f21b4bee7d6e2eeb53db6e935e3b513a

### Produção

- Status: Ready
- Health: Green
- VersionLabel: github-452dc274f21b4bee7d6e2eeb53db6e935e3b513a

Os dois ambientes estão executando a mesma versão da aplicação, confirmando que a versão validada em staging foi posteriormente implantada em produção.