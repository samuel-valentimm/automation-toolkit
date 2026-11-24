# Automation Toolkit

Ferramenta de automação desenvolvida em Python para criação e gerenciamento de backups, limpeza de arquivos antigos e registro de operações.

O Automation Toolkit permite selecionar um diretório, compactar seus arquivos em ZIP e gerenciar os backups gerados por meio de uma interface de linha de comando (CLI).

## Funcionalidades

- [x] Criação de backups compactados em ZIP.
- [x] Inclusão de arquivos e subdiretórios no backup.
- [x] Registro de operações e erros em logs.
- [x] Limpeza de backups com mais de 30 dias.
- [x] Preservação do backup mais recente.
- [x] Consulta de status e espaço ocupado pelos backups.
- [x] Interface de linha de comando interativa.
- [ ] Configurações personalizadas.
- [ ] Limpeza automática opcional ao iniciar o aplicativo.
- [ ] Restauração de backups.

## Tecnologias

- Python 3.10 ou superior.
- Pytest 9.2.0.

## Instalação

### 1. Pré-requisitos

Certifique-se de possuir Python instalado no computador.

### 2. Clonar o repositório

```powershell
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```powershell
cd automation-toolkit
```

### 3. Criar ambiente virtual

```powershell
python -m venv .venv
```

Ativar o ambiente virtual no Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar dependências

```powershell
pip install -r requirements.txt
```

## Como utilizar

### Iniciar o programa

Na pasta principal do projeto, execute:

```powershell
python .\src\cli.py
```

O programa apresentará o