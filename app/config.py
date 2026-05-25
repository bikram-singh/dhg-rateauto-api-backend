import os
from google.cloud import secretmanager


def get_secret(secret_id: str, project_id: str) -> str:
    """Fetch a secret value from GCP Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


class Settings:
    PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "dhg-vaccine-rateauto-nonpord")
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    PORT: int = int(os.getenv("PORT", "8080"))

    # PostgreSQL via PSC
    DB_HOST: str = os.getenv("DB_HOST", "10.10.0.3")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "dhg-vaccinefee-db")
    DB_USER: str = os.getenv("DB_USER", "dhg-vaccinefee-user")
    SECRET_NAME: str = os.getenv("DB_SECRET_NAME", "dhg-vaccinefee-secret")

    @property
    def DB_PASSWORD(self) -> str:
        return get_secret(self.SECRET_NAME, self.PROJECT_ID)

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
