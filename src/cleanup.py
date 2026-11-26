from pathlib import Path
from datetime import datetime, timedelta
from logger import logger
from config import load_config


def get_backups():
    project_root = Path(__file__).resolve().parent.parent
    backup_dir = project_root / "backups"

    backups = list(backup_dir.glob("*.zip"))

    return backups


def get_backup_age(backup):
    modified_time = datetime.fromtimestamp(backup.stat().st_mtime)
    age = datetime.now() - modified_time

    if age < timedelta(0):
        logger.warning(
            f"Data de modificacao futura detectada: {backup.name}. "
            "Arquivo preservado por seguranca."
        )

        return None
    
    return age


def handle_empty_or_single_backup(backups, retention_days):
    if not backups:
        logger.info("Nenhum backup encontrado.")
        return True

    if len(backups) == 1:
        backup = backups[0]
        age = get_backup_age(backup)

        if age is None:
            logger.warning(
                f"Backup preservado por data inconsistente: {backup.name}."
            )
            
            return True
        
        if age > timedelta(days=retention_days):
            logger.warning(
                f"O unico backup esta fora do prazo. "
                f"Preservando por seguranca: {backup.name}"
            )
        else:
            logger.info(f"Existe apenas um backup dentro do prazo: {backup.name}")

        return True

    return False


def classify_backups(backups, retention_days):
    latest_backup = max(backups, key = lambda backup: backup.stat().st_mtime)
    old_backups = []

    for backup in backups:
        age = get_backup_age(backup)

        if age is None:
            logger.info(f"Backup preservado por data inconsistente: {backup.name}")
            continue
        
        logger.info(f"Verificando arquivo: {backup.name} | Idade: {age}")

        if backup == latest_backup:

            if age > timedelta(days = retention_days):
                logger.warning(
                    "Todos os backups estao fora do prazo. "
                    f"Preservando o mais recente: {backup.name}"
                )
            else: 
                logger.info(f"Backup mais recente preservado: {backup.name}")

        elif age > timedelta(days = retention_days):
            old_backups.append(backup) 
            logger.info(f"Backup antigo identificado: {backup.name}")

        else:
            logger.info(f"Backup dentro do prazo: {backup.name}")

    return old_backups


def check_old_backups():

    try:
        config = load_config()

    except ValueError:
        logger.exception("Configuracao invalida. Limpeza cancelada.")
        return

    if config is None:
        logger.warning("Configuracao nao encontrada. Limpeza cancelada.")
        return

    retention_days = config["retention_days"]

    backups = get_backups()

    if handle_empty_or_single_backup(backups, retention_days):
        return

    old_backups = classify_backups(backups, retention_days)

    logger.info(f"Backups antigos encontrados: {len(backups)}")

    delete_old_backups(old_backups)
    

def delete_old_backups(old_backups):
    for backup in old_backups:

        try:
            backup.unlink()
            logger.info(f"Backup removido com sucesso: {backup.name}")

        except FileNotFoundError:
            logger.warning(f"Backup nao encontrado para exclusao: {backup.name}")

        except OSError:
            logger.exception(f"Erro ao remover o backup: {backup.name}")

if __name__ == "__main__":
    check_old_backups()