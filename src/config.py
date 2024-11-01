from datetime import timedelta
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: str
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    JWT_SECRET: str
    ACCESS_TOKEN_TTL: int
    REFRESH_TOKEN_TTL: int
    MAX_ACTIVE_USER_SESSIONS_COUNT: int

    @property
    def database_url_psycopg(self):
        return "postgresql+psycopg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            name=self.DB_NAME,
        )

    @property
    def test_database_url_psycopg(self):
        return "postgresql+psycopg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.TEST_DB_USER,
            password=self.TEST_DB_PASS,
            host=self.TEST_DB_HOST,
            port=self.TEST_DB_PORT,
            name=self.TEST_DB_NAME,
        )

    @property
    def access_token_ttl_timedelta(self):
        return timedelta(seconds=self.ACCESS_TOKEN_TTL)

    @property
    def refresh_token_ttl_timedelta(self):
        return timedelta(seconds=self.REFRESH_TOKEN_TTL)

    model_config = SettingsConfigDict(env_file=Path(__file__).parent / '.env')


settings = Settings()
