import logging
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

log_dir = project_root / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / "automation.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("automation")