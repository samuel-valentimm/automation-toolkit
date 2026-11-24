# Automation Toolkit

Ferramenta de automação desenvolvida em Python para criação e gerenciamento de backups, limpeza de arquivos antigos e registro de operações.

O Automation Toolkit permite selecionar um diretório, compactar seus arquivos em formato ZIP e gerenciar os backups gerados por meio de uma interface de linha de comando (CLI).

## Funcionalidades

- [x] Criação de backups compactados em ZIP.
- [x] Inclusão de arquivos e subdiretórios no backup.
- [x] Validação do diretório de origem.
- [x] Registro de operações e erros em logs.
- [x] Limpeza de backups com mais de 30 dias.
- [x] Preservação do backup mais recente durante a limpeza.
- [x] Consulta da quantidade de backups e do espaço ocupado.
- [x] Interface de linha de comando interativa.
- [x] Testes automatizados com Pytest.
- [ ] Configurações personalizadas.
- [ ] Limpeza automática opcional ao iniciar o aplicativo.
- [ ] Restauração de backups.

## Tecnologias

- Python 3.10 ou superior.
- Pytest 9.2.0.

## Instalação

### 1. Pré-requisitos

Certifique-se de possuir o Python 3.10 ou superior instalado.

### 2. Clonar o repositório

```powershell
git clone https://github.com/samuel-valentimm/automation-toolkit.git
```

Entre na pasta do projeto:

```powershell
cd automation-toolkit
```

### 3. Criar o ambiente virtual

```powershell
python -m venv .venv
```

Ativar o ambiente virtual no Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```powershell
pip install -r requirements.txt
```

## Como utilizar

### Iniciar o programa

Na pasta principal do projeto, execute:

```powershell
python .\src\cli.py
```

O programa apresentará um menu interativo com as seguintes opções:

```text
==============================
      AUTOMATION TOOLKIT V1.0
==============================
1. Criar backup
2. Limpar backups antigos
3. Consultar status
4. Sair
```

### Criar backup

Selecione a opção 1 e informe o caminho do diretório que deseja copiar.

O programa irá percorrer os arquivos e subdiretórios, compactando seu conteúdo em um arquivo ZIP.

Os backups são armazenados na pasta `backups/`, com nomes que incluem a data e o horário de criação.

O diretório original não é alterado durante esse processo.

### Limpar backups antigos

Selecione a opção 2 para iniciar a limpeza manual.

O sistema identifica backups com mais de 30 dias e os remove, preservando sempre o backup mais recente.

A limpeza atua exclusivamente sobre os arquivos ZIP armazenados na pasta de backups do próprio Automation Toolkit.

### Consultar status

Selecione a opção 3 para consultar informações sobre os backups existentes, incluindo:

- Quantidade de backups armazenados.
- Nome do backup mais recente.
- Data e horário do último backup.
- Espaço total ocupado pelos arquivos ZIP.

## Logs

O Automation Toolkit registra suas operações e erros para facilitar o acompanhamento e a identificação de possíveis problemas.

Os registros são armazenados em:

```text
logs/automation.log
```

Os logs incluem informações sobre a execução dos backups, operações de limpeza e erros encontrados durante o processamento.

## Testes automatizados

O projeto utiliza Pytest para verificar o funcionamento das funcionalidades implementadas.

Para executar os testes, entre na pasta `tests`:

```powershell
cd tests
```

Execute:

```powershell
pytest -v
```

Os testes verificam os processos de criação e limpeza de backups, incluindo validações e situações de erro.

## Estrutura do projeto

```text
automation-toolkit/
│
├── src/
│   ├── backup.py
│   ├── cleanup.py
│   ├── cli.py
│   └── logger.py
│
├── tests/
│   ├── test_backup.py
│   └── test_cleanup.py
│
├── backups/          # Criada durante a execução
├── logs/             # Criada durante a execução
│
├── .gitignore
├── README.md
└── requirements.txt
```

### Principais módulos

- **backup.py:** responsável pela criação e compactação dos backups.
- **cleanup.py:** responsável pela identificação e remoção de backups antigos.
- **cli.py:** disponibiliza o menu interativo e conecta as funcionalidades.
- **logger.py:** configura o registro de operações e erros.
- **tests/:** contém os testes automatizados do projeto.

## Segurança e observações

- A limpeza remove somente arquivos ZIP da pasta `backups/` gerenciada pelo Automation Toolkit.
- Os arquivos originais do diretório selecionado não são removidos durante a criação do backup.
- O backup mais recente é preservado durante a limpeza.
- A limpeza é executada manualmente pelo usuário na versão atual.
- Recomenda-se manter cópias dos backups em outro dispositivo ou local de armazenamento para maior segurança.

## Melhorias futuras

Algumas funcionalidades planejadas para versões futuras:

- Configurações personalizadas de retenção.
- Opção para executar a limpeza automaticamente ao iniciar o aplicativo.
- Restauração de backups.
- Verificação da integridade dos arquivos.
- Suporte a outros formatos de compactação.
- Melhorias na interface e na experiência de utilização.

## Status do projeto

**Versão 1.0 — Em desenvolvimento.**

O Automation Toolkit é um projeto de portfólio desenvolvido para praticar Python, automação de arquivos, organização de módulos, tratamento de exceções, logging, testes automatizados e controle de versão com Git.