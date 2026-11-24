from backup import create_backup
from datetime import datetime
from logger import logger
from cleanup import check_old_backups, get_backups

def show_menu():
    print("\n==============================")
    print("      AUTOMATION TOOLKIT V1.0")
    print("==============================")
    print("1. Criar backup")
    print("2. Limpar backups antigos")
    print("3. Consultar status")
    print("4. Sair")


def get_user_choice():
    choice = input("\nEscolha uma opcao: ")
    return choice


def run_backup():
    source = input("\nInforme o diretorio para o backup: ")

    try:
        backup = create_backup(source)
        print(f"\nBackup criado com sucesso: {backup}")

    except (FileNotFoundError, NotADirectoryError, ValueError) as error:
        print(f"\nErro: {error}")

    except Exception:
        logger.exception("Erro inesperado durante a execucao do backup pela CLI.")
        print("\nOcorreu um erro inesperado ao criar o backup. Consulte o arquivo de log.")


def run_cleanup():
    print("\nIniciando limpeza de backups antigos...")
    check_old_backups()
    print("\nProcesso de limpeza finalizado.")


def run_status():
    backups = get_backups()

    if not backups:
        print("\nNehum backup encontrado.")
        return

    total_backups = len(backups)
    latest_backup  = max(
        backups,
        key = lambda backup: backup.stat().st_mtime
    )

    latest_date = datetime.fromtimestamp(
        latest_backup.stat().st_mtime
    ).strftime("%d/%m/%Y %H:%M:%S")

    total_size = sum(
        backup.stat().st_size for backup in backups
    )
    total_size_mb = total_size / (1024 * 1024)

    print("\n========== STATUS DOS BACKUPS ==========")
    print(f"Quantidade de backups: {total_backups}")
    print(f"Backup mais recente: {latest_backup.name}")
    print(f"Data do último backup: {latest_date}")
    print(f"Espaço ocupado: {total_size_mb:.2f} MB")
    print("========================================")


def main():
    while True:
        show_menu()
        choice = get_user_choice()

        match choice:
            case "1":
                run_backup()

            case "2":
                run_cleanup()

            case "3":
                run_status()

            case "4":
                print("\nEncerrando Automation Toolkit...")
                break

            case _:
                print("\nOpcao invalida! Tente novamente.")


if __name__ == "__main__":
    main()