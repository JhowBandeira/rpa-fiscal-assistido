# RPA Fiscal Assistido

Aplicacao desktop Windows para automatizar rotinas fiscais repetitivas, com foco em execucao assistida, checkpoints e organizacao por empresa/competencia.

## Problema

Rotinas fiscais em portais e sistemas desktop exigem muitos passos manuais: acessar sistemas, navegar por menus, baixar arquivos, conferir competencias e retomar execucoes interrompidas. Isso consome tempo e aumenta risco de erro operacional.

## Solucao

O projeto implementa uma base de RPA assistido em Python, com interface desktop, cadastro de empresas/filiais/inscricoes, controle de credenciais, historico de execucao, checkpoints e automacoes para fluxos fiscais. O robo executa rotinas ensinadas, mas nao toma decisao tributaria.

## Tecnologias

- Python
- PySide6
- SQLAlchemy
- Playwright
- pywinauto
- pyautogui
- pypdf
- SQLite local

## Funcionalidades presentes no codigo

- Interface desktop em PySide6.
- Cadastro de empresas, filiais, competencias e inscricoes.
- Camadas de models, repositories e services.
- Execucao de tarefas com checkpoints.
- Modulos de automacao para navegador e sistemas fiscais.
- Workers para execucoes em segundo plano.
- Estrutura para treinamento/registro de fluxos.

## Principios do projeto

- O robo executa; nao toma decisao tributaria.
- Rotinas nao ensinadas ficam pendentes de treinamento.
- Execucoes usam checkpoints persistentes para retomar do ponto de parada.
- Arquivos operacionais devem ser organizados por empresa e competencia.

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

## Observacao de seguranca

Bancos locais, logs, storage, ambientes virtuais e scripts com nome de empresa especifica foram removidos desta publicacao.
