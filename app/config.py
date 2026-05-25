import os


class Settings:
    PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "dhg-vaccine-rateauto-nonpord")
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    PORT: int = int(os.getenv("PORT", "8080"))

    # PostgreSQL via PSC - all from K8s Secret env vars
    DB_HOST: str = os.getenv("DB_HOST", "10.10.0.3")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "dhg-vaccinefee-db")
    DB_USER: str = os.getenv("DB_USER", "dhg-vaccinefee-user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")


settings = Settings()
