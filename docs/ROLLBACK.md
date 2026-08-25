# Estratégia de rollback

O deploy da aplicação utiliza versões identificadas pelo padrão:

`github-<GITHUB_SHA>`

Cada versão corresponde a um commit específico do repositório. Isso permite identificar rapidamente qual versão estava estável antes de uma falha.

## Quando executar um rollback

O rollback deve ser considerado quando, após um deploy, forem identificados problemas como:

- falha de inicialização da aplicação;
- erro crítico em endpoints;
- indisponibilidade do ambiente;
- regressão funcional;
- falha de integração com banco de dados;
- comportamento inesperado identificado após a publicação.

## Processo de rollback

### 1. Identificar a última versão estável

Primeiro, deve-se identificar no GitHub Actions qual foi o último workflow concluído com sucesso antes da versão problemática.

A partir desse workflow, deve-se obter o commit correspondente.

Exemplo:

`github-<SHA_DO_COMMIT_ESTAVEL>`

### 2. Confirmar se a versão existe no Elastic Beanstalk

A versão pode ser consultada utilizando AWS CLI:

```bash
aws elasticbeanstalk describe-application-versions \
  --application-name lacrei-prod \
  --version-label github-<SHA_DO_COMMIT_ESTAVEL>