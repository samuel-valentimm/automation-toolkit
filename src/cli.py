from backup import create_backup
from datetime import datetime
from logger import logger
from cleanup import check_old_backups, get_backups
from config import (
    load_config,
    save_config,
    reset_config,
    repair_config,
    load_config_raw,
    get_invalid_config_fields,
    DEFAULT_CONFIG,
    ALLOWED_RETENTION_DAYS
)

def show_menu():
    print("\n==============================")
    print("      AUTOMATION TOOLKIT V2.0")
    print("==============================")
    print("1. Criar backup")
    print("2. Limpar backups antigos")
    print("3. Consultar status")
    print("4. Configuracoes")
    print("5. Sair")

def show_restricted_menu():
    print("\n==============================")
    print("   AUTOMATION TOOLKIT V2.0")
    print("       MODO RESTRITO")
    print("==============================")
    print("1. Criar backup")
    print("2. Consultar status")
    print("3. Recuperar configuracao")
    print("4. Sair")


def run_config_recovery():
    try:
        config = load_config_raw()

    except ValueError as error:
        print(f"\nErro ao carregar a configuracao: {error}")
        return

    if config is None:
        print("\nNenhuma configuracao encontrada para recuperar.")
        return

    invalid_fields = get_invalid_config_fields(config)
    print("\nCampos que precisam de recuperacao:")

    for field in invalid_fields:
        print(f"- {field}")

    if not invalid_fields:
        print("\nA configuracao ja esta valida. Nenhuma recuperacao necessaria.")
        return

    if "estrutura" in invalid_fields:
        print("\nA estrutura do arquivo nao permite correcao individual.")
        print("\n1. Restaurar configuracao padrao")
        print("2. Voltar")

    else:
        print("\nOpcoes de recuperacao:")
        print("1. Corrigir campos invalidos")
        print("2. Restaurar configuracao padrao")
        print("3. Voltar")

    choice = input("\nEscolha uma opcao: ")

    max_option = 2 if "estrutura" in invalid_fields else 3

    while not choice.isdigit() or not 1 <= int(choice) <= max_option:
        print("\nOpcao invalida! Tente novamente.")
        choice = input("\nEscolha uma opcao: ")

    if ("estrutura" in invalid_fields and choice == "2") or ( "estrutura" not in invalid_fields and choice == "3"):
        print("\nRetornando ao menu...")
        return


def show_config_menu():
    try:
        config = load_config()

    except ValueError as error:
        print(f"\nErro na configuracao: {error}")
        return

    if config is None:
            print("\nConfiguracao nao encontrada.")
            print("\n1. Criar configuracao inicial")
            print("2. Voltar")

            choice = input("\nEscolha uma opcao: ")

            while choice not in ("1", "2"):
                print("\nOpcao invalida! Tente novamente.")
                choice = input("\nEscolha uma opcao: ")

            if choice == "1":
                config = DEFAULT_CONFIG.copy()
                save_config(config)
                print("\nConfiguracao criada com sucesso!")

            else:
                return
            
    while True:
        print("\n========== CONFIGURACOES ==========")
        print(f"Periodo de retencao: {config['retention_days']} dias")

        status = "Ativada" if config["cleanup_on_startup"] else "Desativada"
        print(f"Limpeza automatica: {status}")

        print("\n1. Alterar periodo de retencao")

        action = "Desativar" if config["cleanup_on_startup"] else "Ativar"
        print(f"2. {action} limpeza automatica.")
        
        print("3. Voltar")

        choice = input("\nEscolha uma opcao: ")

        match choice:
            case "1":
                change_retention(config)

            case "2":
                config["cleanup_on_startup"] = not config["cleanup_on_startup"]
                save_config(config)

                status = "ativada" if config["cleanup_on_startup"] else "desativada"
                print(f"\nLimpeza automatica {status} com sucesso!")

            case "3":
                break

            case _:
                print("Opcao invalida!")


def change_retention(config):
    print("\n========== PERIODO DE RETENCAO ==========")
    print(f"Periodo atual: {config['retention_days']} dias")

    for index, days in enumerate(ALLOWED_RETENTION_DAYS, start = 1):
        print(f"{index}. {days} dias")

    print(f"{len(ALLOWED_RETENTION_DAYS) + 1}. Voltar")

    choice =  input("\nEscolha uma opcao: ")

    while not choice.isdigit() or not 1 <= int(choice) <= len(ALLOWED_RETENTION_DAYS) + 1:
        print("\nOpcao invalida! Tente novamente.")
        choice = input("\nEscolha uma opcao: ")

    match choice:
        case "7":
            return

        case _:
            selected_days = ALLOWED_RETENTION_DAYS[int(choice) - 1]

            if selected_days == config["retention_days"]:
                print("\nPeriodo escolhido igual ao anterior.")
                print(f"Mantendo periodo atual: {selected_days} dias.")
                return

            config["retention_days"] = selected_days
            save_config(config)

            print(f"\nPeriodo de retencao alterado para {selected_days} dias!")


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
    try:
        config = load_config()

    except ValueError:
        logger.exception("Configuracao invalida. limpeza manual cancelada.")
        print("\nConfiguracao invalida. Limpeza cancelada.")
        return

    if config is None:
        print("\nConfiguracao nao encontrada. Crie uma configuracao antes de limpar os backups.")
        return
    
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
    restricted_mode = False

    try:
        config = load_config()

    except ValueError:
        restricted_mode = True
        logger.exception("Configuracao invalida. Limpeza automatica ignorada.")

    else:
        if config is not None and config["cleanup_on_startup"]:
            print("\nExecutando limpeza automatica...")
            check_old_backups()

    while True:
        if restricted_mode:
            show_restricted_menu()

        else:
            show_menu()

        choice = get_user_choice()

        if restricted_mode:
            match choice:

                case "1":
                    run_backup()

                case "2":
                    run_status()

                case "3":
                    print("\nRecuperacao de configuracao ainda nao implementada.")

                case "4":
                    print("\nEncerrando Automation Toolkit...")
                    break

                case _:
                    print("Opcao invalida! Tente novamente.")

        else:
            match choice:

                case "1":
                    run_backup()

                case "2":
                    run_cleanup()

                case "3":
                    run_status()

                case "4":
                    show_config_menu()

                case "5":
                    print("\nEncerrando Automation Toolkit...")
                    break

                case _:
                    print("\nOpcao invalida! Tente novamente.")


if __name__ == "__main__":
    main()