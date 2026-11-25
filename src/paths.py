from pathlib import Path

documents_dir = Path.home() / "Documents"

data_dir = documents_dir / "Automation Toolkit"

backup_dir = data_dir / "backups"
log_dir = data_dir / "logs"
config_file = data_dir / "config.json"

data_dir.mkdir(parents = True, exist_ok = True)
backup_dir.mkdir(exist_ok = True)
log_dir.mkdir(exist_ok = True)
