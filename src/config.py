from paths import config_file
import json


DEFAULT_CONFIG = {
    "retention_days": 30,
    "cleanup_on_startup": False
}

ALLOWED_RETENTION_DAYS = [1, 3, 7, 15, 30, 60]


def save_config(config):
    if not validate_config(config):
        raise ValueError("Nao e possivel salvar uma configuracao invalda.")

    config_file.parent.mkdir(parents = True, exist_ok = True)
    
    with open(config_file, "w", encoding = "utf-8") as file:
        json.dump(config, file, indent = 4)


def load_config():
    if not config_file.exists():
        return None

    try:
        with open(config_file, "r", encoding = "utf-8") as file:
            config = json.load(file)

    except json.JSONDecodeError:
        raise ValueError("O arquivo de configuracao esta corrompido.")

    if not validate_config(config):
        raise ValueError("Arquivo de configuracao possui valores invalidos.")

    return config 


def get_invalid_config_fields(config):
    if not isinstance(config, dict):
        return ["estrutura"]

    invalid_fields = []

    retention_days = config.get("retention_days")
    cleanup_on_startup = config.get("cleanup_on_startup")

    if type(retention_days) is not int or retention_days not in ALLOWED_RETENTION_DAYS:
        invalid_fields.append("retention_days")

    if not isinstance(cleanup_on_startup, bool):
        invalid_fields.append("cleanup_on_startup")

    return invalid_fields


def validate_config(config):
    return len(get_invalid_config_fields(config)) == 0