# Estratégia de Rollback

O deploy da aplicação utiliza versões identificadas pelo padrão:

`github-SEU_SHA_ESTAVEL`

Cada versão corresponde a um commit específico do repositório. Dessa forma, uma versão anterior da aplicação pode ser restaurada utilizando o Elastic Beanstalk.

## Quando executar um rollback

O rollback deve ser considerado quando, após um deploy, forem identificados problemas como:

- falha de inicialização da aplicação;
- erro crítico em endpoints;
- indisponibilidade do ambiente;
- regressão funcional;
- falha de integração com o banco de dados;
- comportamento inesperado após a publicação.

## 1. Identificar a última versão estável

Acesse o histórico do GitHub Actions:

https://github.com/Iverzada/lacrei-api/actions

Localize a última execução concluída com sucesso antes da versão problemática e copie o SHA do commit correspondente.

As versões do Elastic Beanstalk seguem o formato:

`github-SEU_SHA_ESTAVEL`

Exemplo:

`github-d32e626abc25b12bbf26f7cd02e64f9bfa1afcf5`

## 2. Confirmar que a versão existe no Elastic Beanstalk

### Produção

No PowerShell, defina a versão que deseja restaurar:

```powershell
$versao="github-SEU_SHA_ESTAVEL"
```

Substitua `SEU_SHA_ESTAVEL` pelo SHA real do commit **apenas quando for necessário executar um rollback**.

Depois confirme se essa versão existe no Elastic Beanstalk:

```powershell
aws elasticbeanstalk describe-application-versions --application-name lacrei-prod --version-labels $versao --query "ApplicationVersions[].VersionLabel" --output table
```

O rollback também pode ser feito pela AWS CLI. Primeiro, deve-se definir a versão estável que será restaurada:

Em produção:

```powershell
aws elasticbeanstalk update-environment --environment-name lacrei-prod --version-label $versao
```

Em staging:

```powershell
aws elasticbeanstalk update-environment --environment-name lacrei-amb --version-label $versao
```

### Staging

Para verificar a mesma versão em staging:

```powershell
aws elasticbeanstalk describe-application-versions --application-name lacrei-api --version-labels $versao --query "ApplicationVersions[].VersionLabel" --output table
```

Se a versão aparecer no resultado, ela está disponível para rollback.

## 3. Executar rollback em produção

Para restaurar uma versão anterior em produção:

```powershell
aws elasticbeanstalk update-environment --environment-name lacrei-prod --version-label $versao
```

Aguarde a conclusão:

```powershell
aws elasticbeanstalk wait environment-updated --environment-names lacrei-prod
```

Depois confirme o estado e a versão implantada:

```powershell
aws elasticbeanstalk describe-environments --environment-names lacrei-prod --query "Environments[0].[Status,Health,VersionLabel]" --output table
```

O resultado esperado após um rollback bem-sucedido é:

- `Status`: `Ready`
- `Health`: `Green`
- `VersionLabel`: versão escolhida para o rollback

## 4. Executar rollback em staging

Para executar o rollback em staging:

```powershell
aws elasticbeanstalk update-environment --environment-name lacrei-amb --version-label $versao
```

Aguarde a conclusão:

```powershell
aws elasticbeanstalk wait environment-updated --environment-names lacrei-amb
```

Depois confirme o estado:

```powershell
aws elasticbeanstalk describe-environments --environment-names lacrei-amb --query "Environments[0].[Status,Health,VersionLabel]" --output table
```

## 5. Validar a aplicação após o rollback

Após o rollback, confirme que a aplicação continua acessível.

### Produção

```powershell
curl.exe -s -o NUL -w "%{http_code}" "http://lacrei-prod.eba-exshdvpe.us-east-2.elasticbeanstalk.com/api/docs/"
```

### Staging

```powershell
curl.exe -s -o NUL -w "%{http_code}" "http://lacrei-amb.eba-ssmpxt2b.us-east-2.elasticbeanstalk.com/api/docs/"
```

O retorno esperado é:

`200`

Também devem ser verificados os principais endpoints e a autenticação da API.

## 6. Migrações de banco de dados

O rollback da aplicação não desfaz automaticamente migrações do banco de dados.

Antes de restaurar uma versão anterior, deve-se verificar se as migrações aplicadas pela versão mais recente são compatíveis com a versão que será restaurada.

Caso uma alteração de banco seja destrutiva ou incompatível, a recuperação deve ser planejada separadamente, utilizando uma migração reversível ou um backup/snapshot previamente criado.

Não é recomendado executar rollback destrutivo de banco de dados sem validação prévia.

## Resumo do procedimento

1. identificar no GitHub Actions o último commit estável;
2. localizar a versão `github-SHA` correspondente no Elastic Beanstalk;
3. confirmar que essa versão está disponível;
4. executar `update-environment` apontando para a versão escolhida;
5. aguardar o ambiente retornar para `Ready`;
6. confirmar que o ambiente está `Green`;
7. confirmar o `VersionLabel`;
8. testar a aplicação e os principais endpoints;
9. verificar a compatibilidade das migrações do banco de dados.

## Evidência de validação do rollback

O procedimento de rollback foi validado manualmente em staging em 25/08/2026.

A versão inicialmente implantada era:

`github-494e84672636c218cb55248e908d1664f5a669ba`

Foi realizado rollback para a versão anterior:

`github-d32e626abc25b12bbf26f7cd02e64f9bfa1afcf5`

Após o rollback, o ambiente apresentou:

- `Status`: `Ready`
- `Health`: `Green`
- documentação da API respondendo com HTTP `200`

Em seguida, staging foi restaurado para:

`github-494e84672636c218cb55248e908d1664f5a669ba`

Após a restauração, o ambiente retornou novamente para `Ready / Green` e a documentação continuou respondendo com HTTP `200`.

Durante todo o procedimento, o ambiente de produção permaneceu na versão atual, saudável e acessível com HTTP `200`.

Dessa forma, o procedimento documentado de rollback foi executado e validado sem alteração do ambiente de produção.