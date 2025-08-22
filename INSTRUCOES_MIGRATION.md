# Instruções para Executar a Migration

## Resumo das Mudanças
Criamos uma migration para:
1. **Remover** o campo `is_responsavel_tecnico` da tabela `users_safs`
2. **Remover** o campo `processo_id` da tabela `itens_catalogo`

## Arquivos Criados
- `C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend\alembic\versions\123abc456def_remover_processo_id_e_is_responsavel_tecnico.py`

## Como Executar a Migration

### Opção 1: Usando o Terminal do Windows
1. Abra o **Prompt de Comando** ou **PowerShell**
2. Execute os seguintes comandos:

```cmd
cd "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
python -m alembic current
python -m alembic upgrade head
python -m alembic current
```

### Opção 2: Usando o Arquivo Batch
1. Execute o arquivo: `C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\execute_migration.bat`

### Opção 3: Usando Python
1. Execute: `python C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\execute_migration.py`

## Verificações Após Execução
Após executar a migration, verifique se:
1. ✅ O campo `is_responsavel_tecnico` foi removido da tabela `users_safs`
2. ✅ O campo `processo_id` foi removido da tabela `itens_catalogo`
3. ✅ Os relacionamentos N:N para responsável técnico ainda estão funcionando
4. ✅ Os relacionamentos N:N para processos ainda estão funcionando

## Rollback (se necessário)
Se precisar desfazer a migration:
```cmd
cd "C:\Users\abimael.souza\Desktop\APLICATIVOS\safs\backend\backend"
python -m alembic downgrade -1
```

## Comandos Úteis do Alembic
- Ver status atual: `python -m alembic current`
- Ver histórico: `python -m alembic history`
- Upgrade para a versão mais recente: `python -m alembic upgrade head`
- Downgrade uma versão: `python -m alembic downgrade -1`