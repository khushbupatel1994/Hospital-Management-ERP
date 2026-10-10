import os
from dataclasses import dataclass

@dataclass(frozen=True)
class EnterpriseConfig:
    database_url: str = os.getenv("ERP_DATABASE_URL", "sqlite:///hospital.db")
    redis_url: str = os.getenv("ERP_REDIS_URL", "")
    backup_dir: str = os.getenv("ERP_BACKUP_DIR", "./backups")
    jwt_secret: str = os.getenv("ERP_JWT_SECRET", "")
    access_minutes: int = int(os.getenv("ERP_ACCESS_MINUTES", "20"))
    refresh_days: int = int(os.getenv("ERP_REFRESH_DAYS", "7"))
    environment: str = os.getenv("ERP_ENV", "development")
    tls_required: bool = os.getenv("ERP_TLS_REQUIRED", "false").lower() == "true"
