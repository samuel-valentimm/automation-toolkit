# Esse modulo e responsavel por:
# Receber diretorio de origem
# Verificar existencia do diretorio
# Percorrer Arquivos e subpastas
# Compctar tudo em zip
# Salvar o backup com data e horario no nome

from logger import logger
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime


def create_backup(source):
    source_path = Path(source)

    if not source_path.exists():
        raise FileNotFoundError("Diretorio de origem nao encontrado.")

    if not source_path.is_dir():
        raise NotADirectoryError("O caminho informado nao e um diretorio.")

    project_root = Path(__file__).resolve().parent.parent
    backup_dir = project_root / "backups"
    backup_dir.mkdir(parents = True, exist_ok = True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.zip"
    backup_path = backup_dir / backup_name

    files = [file for file in source_path.rglob("*") if file.is_file()]

    if not files:
        raise ValueError("O diretorio nao possui arquivos para o backup.")

    try:
        logger.info(f"Iniciando backup de: {source_path}")

        with ZipFile(backup_path, "w", ZIP_DEFLATED) as zip_file:
                for file in files:
                    zip_file.write(file, file.relative_to(source_path))
        
        logger.info(f"Backup criado com sucesso: {backup_path}")

    except Exception:
        logger.exception("Erro ao criar o backup.")
        if backup_path.exists():
             backup_path.unlink()
             logger.info("Arquivo de backup incompleto removido!")
        raise

    return backup_path