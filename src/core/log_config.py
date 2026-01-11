from dataclasses import dataclass
from pathlib import Path
from typing import Final
import os


ROOT_PROJ: Final[Path] = Path(__file__).parent.parent.parent


@dataclass(frozen=True)
class LogConfig:
    directory: Path = ROOT_PROJ / "logs"
    level: str = os.getenv("LOG_LEVEL", "INFO")
    rotation: str = os.getenv("LOG_ROTATION_SIZE", "150 MB")
    retention: str = os.getenv("LOG_RETENTION_DAYS", "10 days")
    format: str = (
        "<level>{level}</level> | "
        "<green>{time:HH:mm:ss}</green> | "
        "{message} "
        "<cyan>({name}:{line})</cyan>"
    )


LOG_CONFIG: Final = LogConfig()